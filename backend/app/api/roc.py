from fastapi import APIRouter, HTTPException
from app.services.evaluation.roc_service import get_roc_curve

router = APIRouter()

@router.get("/{dataset_name}/{model_name}")
def roc(dataset_name: str, model_name: str):

    result = get_roc_curve(
        dataset_name,
        model_name
    )

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = "ROC curve not found."
        )

    return result