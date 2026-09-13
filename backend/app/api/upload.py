import re
import threading
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import settings
from app.services.dataset_service import analyze_dataset
from app.services.preprocessing.preprocessing_service import preprocess_dataset
from app.services.preprocessing.input_schema import build_input_schema
from app.services.model_training.trainer import train_model
from app.services.model_training.evaluator import evaluate_model
from app.services.persistence.model_saver import save_model
from app.services.jobs import job_manager
from app.core.deps import get_current_user
from app.database.models import User
from app.core.ownership import owner_prefix

router = APIRouter(prefix="/upload", tags=["Upload"], dependencies=[Depends(get_current_user)])

UPLOAD_FOLDER = settings.UPLOAD_DIR
UPLOAD_FOLDER.mkdir(exist_ok=True)


def _secure_filename(filename: str) -> str:
    """
    Sanitize a user-supplied filename: strip any directory components (path
    traversal protection) and only allow a safe character set.
    """
    name = Path(filename).name  # drops any ../ or absolute path components
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name:
        raise HTTPException(status_code=400, detail="Invalid filename.")
    return name


def _validate_upload(file: UploadFile, contents: bytes) -> str:
    filename = _secure_filename(file.filename or "")
    extension = Path(filename).suffix.lower()

    if extension not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. "
                   f"Allowed types: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}",
        )

    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File is too large ({size_mb:.1f} MB). "
                   f"Maximum allowed size is {settings.MAX_UPLOAD_SIZE_MB} MB.",
        )

    return filename


def _read_dataset(file_path: Path) -> pd.DataFrame:
    extension = file_path.suffix.lower()
    try:
        if extension in (".xlsx", ".xls"):
            return pd.read_excel(file_path)
        return pd.read_csv(file_path)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be read as a dataset. "
                   "Please make sure it is a valid CSV or Excel file.",
        ) from exc


@router.post("/")
async def upload_dataset(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Step 1 of the workflow: upload a dataset and get back a data-quality
    analysis plus a *recommended* target column.

    This endpoint does NOT train anything. Training only happens once the
    user (or caller) explicitly confirms a target column via POST
    /upload/train(/start) - MLForge never silently assumes the target when
    there is ambiguity.

    The stored filename is namespaced to the uploading user
    (`u{user_id}_...`) so later steps can verify ownership by prefix alone,
    without a database lookup.
    """

    contents = await file.read()
    raw_filename = _validate_upload(file, contents)
    filename = f"{owner_prefix(current_user.id)}{raw_filename}"

    file_path = UPLOAD_FOLDER / filename
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    df = _read_dataset(file_path)

    if len(df) < settings.MIN_ROWS_REQUIRED:
        raise HTTPException(
            status_code=400,
            detail=f"Dataset has only {len(df)} rows. "
                   f"At least {settings.MIN_ROWS_REQUIRED} rows are required "
                   f"to train a reliable model.",
        )

    if df.shape[1] < 2:
        raise HTTPException(
            status_code=400,
            detail="Dataset must contain at least two columns "
                   "(one target column and at least one feature column).",
        )

    analysis = analyze_dataset(df)

    return {
        "filename": filename,
        "message": "File uploaded successfully. Please confirm a target column to begin training.",
        "rows": len(df),
        "columns": df.shape[1],
        "analysis": analysis,
    }


class TrainRequest(BaseModel):
    filename: str
    target_column: str
    training_mode: str = "balanced"  # fast | balanced | thorough


def _run_training_pipeline(df: pd.DataFrame, filename: str, request: TrainRequest, user_id: int, on_progress=None) -> dict:
    """
    The full preprocess -> train -> evaluate -> persist pipeline, shared by
    both the synchronous and background-job training endpoints.
    """

    analysis = analyze_dataset(df, target_column=request.target_column)

    preprocessing_result = preprocess_dataset(df, analysis)

    training_result = train_model(
        preprocessing_result["X"],
        preprocessing_result["y"],
        analysis,
        pipeline=preprocessing_result["pipeline"],
        feature_names=preprocessing_result["feature_names"].tolist(),
        label_encoder=preprocessing_result.get("label_encoder"),
        training_mode=request.training_mode,
        on_progress=on_progress,
    )

    evaluation = evaluate_model(training_result)

    # `filename` is already namespaced as "u{user_id}_{original_name}.ext"
    # (see upload_dataset) - reuse that as the storage/dataset key directly,
    # and keep a clean display_name (prefix stripped) for the UI.
    dataset_name = filename.rsplit(".", 1)[0]
    prefix = owner_prefix(user_id)
    display_name = dataset_name[len(prefix):] if dataset_name.startswith(prefix) else dataset_name

    input_schema = build_input_schema(df, analysis)

    for trained_model in training_result["trained_models"]:

        model_name = trained_model["model_name"]

        model_eval = next(
            (r for r in evaluation["all_models"] if r["model_name"] == model_name),
            None,
        )

        if model_eval is None:
            continue

        if analysis["problem_type"] == "Regression":
            performance = model_eval["r2_score"]
        else:
            performance = model_eval["accuracy"]["value"]

        X_train = training_result["X_train"]
        rng = np.random.default_rng(seed=42)
        sample_size = min(settings.SHAP_BACKGROUND_SAMPLE_SIZE, len(X_train))
        indices = rng.choice(len(X_train), size=sample_size, replace=False)

        save_model(
            model=trained_model["model"],
            pipeline=preprocessing_result["pipeline"],
            label_encoder=preprocessing_result.get("label_encoder"),
            feature_names=preprocessing_result["feature_names"].tolist(),
            metadata={
                "model_name": model_name,
                "problem_type": analysis["problem_type"],
                "algorithm": type(trained_model["model"]).__name__,
                "target_column": analysis["target_column"],
                "feature_count": len(preprocessing_result["feature_names"]),
                "dataset_name": dataset_name,
                "display_name": display_name,
                "owner_id": user_id,
                "performance": performance,
                "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mlforge_version": settings.APP_VERSION,
                "input_schema": input_schema,
            },
            dataset_name=dataset_name,
            model_name=model_name,
            evaluation=model_eval,
            background_data=X_train[indices],
            roc_curve=trained_model["roc_curve"],
            confusion_matrix=trained_model["confusion_matrix"],
            tuned=trained_model["tuned"],
            best_params=trained_model["best_params"],
            best_cv_score=trained_model["best_cv_score"],
        )

    return {
        "filename": filename,
        "dataset_name": dataset_name,
        "display_name": display_name,
        "message": "Training completed successfully.",
        "analysis": analysis,
        "preprocessing": preprocessing_result["summary"],
        "training": {
            "problem_type": training_result["problem_type"],
            "models_trained": [m["model_name"] for m in training_result["trained_models"]],
            "models_skipped": training_result.get("skipped_models", []),
        },
        "evaluation": evaluation,
    }


def _load_and_validate(request: TrainRequest, current_user: User) -> pd.DataFrame:
    filename = _secure_filename(request.filename)

    if not filename.startswith(owner_prefix(current_user.id)):
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{request.filename}' was not found. Please upload it again.",
        )

    file_path = UPLOAD_FOLDER / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{filename}' was not found. Please upload it again.",
        )

    df = _read_dataset(file_path)

    if request.target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{request.target_column}' does not exist in this dataset.",
        )

    return df


@router.post("/train")
def train_from_upload(request: TrainRequest, current_user: User = Depends(get_current_user)):
    """
    Synchronous training (blocks until finished). Useful for small
    datasets, scripting, and tests. For a real UI with live progress, use
    POST /upload/train/start + GET /jobs/{job_id} instead.
    """
    request.filename = _secure_filename(request.filename)
    df = _load_and_validate(request, current_user)
    return _run_training_pipeline(df, request.filename, request, current_user.id)


@router.post("/train/start")
def start_training_job(request: TrainRequest, current_user: User = Depends(get_current_user)):
    """
    Kick off training in a background thread and return immediately with a
    job_id. Poll GET /jobs/{job_id} for real, backend-driven progress
    (each stage reported corresponds to an actual model actually being
    trained - never a decorative/fake progress bar).
    """
    request.filename = _secure_filename(request.filename)
    df = _load_and_validate(request, current_user)  # validate up front so failures surface immediately

    job_id = job_manager.create_job(owner_id=current_user.id)
    user_id = current_user.id

    def run():
        try:
            def on_progress(stage, current, total):
                job_manager.set_progress(job_id, stage, current, total)

            result = _run_training_pipeline(df, request.filename, request, user_id, on_progress=on_progress)
            job_manager.complete_job(job_id, result)
        except Exception as exc:
            job_manager.fail_job(job_id, str(exc))

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    return {"job_id": job_id}
