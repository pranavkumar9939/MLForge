from fastapi import APIRouter

from app.services.model_registry.registry_service import get_model_versions
from app.services.prediction.prediction_history_service import load_prediction_history

router = APIRouter(
    prefix="/prediction-history",
    tags = ["Prediction History"]
)

@router.get("/{dataset_name}/{model_name}")
def get_history(
    dataset_name: str,
    model_name: str
):

    registry = get_model_versions(
        dataset_name,
        model_name
    )

    production_version = registry.get(
        "production"
    )

    if production_version is None:

        return {
            "dataset_name": dataset_name,
            "model_name": model_name,
            "version": None,
            "history": []
        }

    history = load_prediction_history(
        dataset_name=dataset_name,
        model_name=model_name,
        version=production_version
    )

    return {

        "dataset_name": dataset_name,

        "model_name": model_name,

        "version": production_version,

        "count": len(history),

        "history": history
    }