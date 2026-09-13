from pathlib import Path
import json

from app.services.persistence.model_loader import get_latest_version_folder

BASE_DIR = Path(__file__).resolve().parents[3]

BASE_MODEL_DIR = BASE_DIR / "saved_models"


def compare_models(dataset_name: str):

    dataset_path = BASE_MODEL_DIR / dataset_name

    if not dataset_path.exists():
        return None

    models = []
    problem_type = None

    for model_folder in dataset_path.iterdir():

        if not model_folder.is_dir():
            continue

        # Models are saved under dataset/model_name/{version}/... - resolve
        # the latest version rather than looking for files directly here
        # (this used to read evaluation.json straight from model_folder,
        # which no longer exists once versioning was introduced).
        try:
            active_folder = Path(get_latest_version_folder(str(dataset_path), model_folder.name))
        except FileNotFoundError:
            continue

        evaluation_file = active_folder / "evaluation.json"
        metadata_file = active_folder / "metadata.json"

        if not evaluation_file.exists() or not metadata_file.exists():
            continue

        with open(evaluation_file) as f:
            evaluation = json.load(f)

        with open(metadata_file) as f:
            metadata = json.load(f)

        if problem_type is None:
            problem_type = metadata["problem_type"]

        if problem_type == "Regression":
            model_result = {
                "model_name": metadata["model_name"],
                "r2_score": evaluation["r2_score"],
                "mae": evaluation["mae"],
                "rmse": evaluation["rmse"],
                "overall_score": evaluation["overall_assessment"]["overall_score"],
                "status": evaluation["overall_assessment"]["status"],
                "color": evaluation["r2_info"]["color"]
            }
        else:
            model_result = {
                "model_name": metadata["model_name"],
                "accuracy": evaluation["accuracy"]["value"],
                "precision": evaluation["precision"]["value"],
                "recall": evaluation["recall"]["value"],
                "f1_score": evaluation["f1_score"]["value"],
                "overall_score": evaluation["overall_assessment"]["overall_score"],
                "status": evaluation["overall_assessment"]["status"],
                "color": evaluation["accuracy"]["color"]
            }

        models.append(model_result)

    models.sort(key=lambda x: x["overall_score"], reverse=True)

    best_model = models[0]["model_name"] if models else None

    return {
        "dataset": dataset_name,
        "problem_type": problem_type,
        "best_model": best_model,
        "models": models
    }
