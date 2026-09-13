import re
import threading
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sklearn.decomposition import PCA

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.ownership import owner_prefix, require_owner
from app.database.models import User
from app.services.preprocessing.unsupervised_preprocessing import preprocess_unsupervised
from app.services.unsupervised.clustering_engine import run_clustering
from app.services.unsupervised.dimensionality_reduction_engine import run_dimensionality_reduction
from app.services.persistence.unsupervised_saver import (
    save_clustering_results,
    save_dimensionality_reduction_results,
    load_clustering_results,
    load_dimensionality_reduction_results,
)
from app.services.jobs import job_manager

router = APIRouter(prefix="/unsupervised", tags=["Unsupervised"])

UPLOAD_FOLDER = settings.UPLOAD_DIR


def _secure_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name:
        raise HTTPException(status_code=400, detail="Invalid filename.")
    return name


class UnsupervisedRequest(BaseModel):
    filename: str
    mode: str  # "clustering" | "dimensionality_reduction"
    n_clusters: int | None = None
    n_components: int = 2


def _load_owned_file(filename: str, current_user: User) -> pd.DataFrame:
    filename = _secure_filename(filename)

    if not filename.startswith(owner_prefix(current_user.id)):
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{filename}' was not found. Please upload it again.",
        )

    file_path = UPLOAD_FOLDER / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{filename}' was not found. Please upload it again.",
        )

    try:
        if file_path.suffix.lower() in (".xlsx", ".xls"):
            return pd.read_excel(file_path)
        return pd.read_csv(file_path)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be read as a dataset.",
        ) from exc


def _run_unsupervised_pipeline(df: pd.DataFrame, filename: str, request: UnsupervisedRequest, user_id: int, on_progress=None) -> dict:
    dataset_name = filename.rsplit(".", 1)[0]
    prefix = owner_prefix(user_id)
    display_name = dataset_name[len(prefix):] if dataset_name.startswith(prefix) else dataset_name

    if on_progress:
        on_progress("Preprocessing dataset", 0, 1)

    try:
        prep = preprocess_unsupervised(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    X = prep["X"]

    metadata = {
        "dataset_name": dataset_name,
        "display_name": display_name,
        "owner_id": user_id,
        "mode": request.mode,
        "preprocessing": prep["summary"],
        "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mlforge_version": settings.APP_VERSION,
    }

    if request.mode == "clustering":
        result = run_clustering(X, k=request.n_clusters, on_progress=on_progress)

        viz_components = min(2, X.shape[1])
        pca = PCA(n_components=viz_components, random_state=42)
        points = pca.fit_transform(X)[:, :2].tolist()

        for r in result["results"]:
            r["labels"] = [int(label) for label in r["labels"]]

        visualization = {"points": points}

        save_clustering_results(dataset_name, metadata, result, visualization)

        return {
            "dataset_name": dataset_name,
            "display_name": display_name,
            "mode": "clustering",
            "recommended_k": result["recommended_k"],
            "best_algorithm": result["best_algorithm"],
            "results": [{k: v for k, v in r.items() if k != "model"} for r in result["results"]],
            "skipped": result["skipped"],
        }

    elif request.mode == "dimensionality_reduction":
        result = run_dimensionality_reduction(X, n_components=request.n_components, on_progress=on_progress)
        save_dimensionality_reduction_results(dataset_name, metadata, result)

        return {
            "dataset_name": dataset_name,
            "display_name": display_name,
            "mode": "dimensionality_reduction",
            "n_components": result["n_components"],
            "results": result["results"],
            "skipped": result["skipped"],
        }

    raise HTTPException(status_code=400, detail="mode must be 'clustering' or 'dimensionality_reduction'.")


@router.post("/train/start")
def start_unsupervised_job(request: UnsupervisedRequest, current_user: User = Depends(get_current_user)):
    """
    Kick off clustering or dimensionality reduction in a background thread.
    Poll GET /jobs/{job_id} for progress, same as supervised training.
    """
    if request.mode not in ("clustering", "dimensionality_reduction"):
        raise HTTPException(status_code=400, detail="mode must be 'clustering' or 'dimensionality_reduction'.")

    df = _load_owned_file(request.filename, current_user)

    if len(df) < settings.MIN_ROWS_REQUIRED:
        raise HTTPException(
            status_code=400,
            detail=f"Dataset has only {len(df)} rows. At least {settings.MIN_ROWS_REQUIRED} rows are required.",
        )

    job_id = job_manager.create_job(owner_id=current_user.id)
    user_id = current_user.id

    def run():
        try:
            def on_progress(stage, current, total):
                job_manager.set_progress(job_id, stage, current, total)

            result = _run_unsupervised_pipeline(df, request.filename, request, user_id, on_progress=on_progress)
            job_manager.complete_job(job_id, result)
        except HTTPException as exc:
            job_manager.fail_job(job_id, str(exc.detail))
        except Exception as exc:
            job_manager.fail_job(job_id, str(exc))

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    return {"job_id": job_id}


@router.get("/clustering/{dataset_name}")
def get_clustering_results(dataset_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)
    result = load_clustering_results(dataset_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Clustering results not found.")
    return result


@router.get("/dimensionality-reduction/{dataset_name}")
def get_dimensionality_reduction_results(dataset_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)
    result = load_dimensionality_reduction_results(dataset_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Dimensionality reduction results not found.")
    return result
