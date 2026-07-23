from fastapi import APIRouter, HTTPException

from app.services.feature_importance.feature_importance_service import get_feature_importance

router = APIRouter(
    prefix = "/feature-importance",
    tags = ["Feature Importance"]
)

@router.get("/{dataset_name}/{model_name}")
def feature_importance(
    dataset_name: str,
    model_name: str,
    top_n: int = 10
):
    """
    Return the top N most important features for a trained model.
    """

    result = get_feature_importance(
        dataset_name = dataset_name,
        model_name = model_name,
        top_n = top_n
    )

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = "Dataset or model not found."
        )

    return result