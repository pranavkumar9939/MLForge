from fastapi import APIRouter, HTTPException

from app.services.evaluation.confusion_matrix_service import get_confusion_matrix

router = APIRouter()

@router.get("/{dataset_name}/{model_name}")
def confusion_matrix(
    dataset_name: str,
    model_name: str
):

    result = get_confusion_matrix(
        dataset_name,
        model_name
    )

    if result is None:

        raise HTTPException(
            status_code = 404,
            detail = "Confusion Matrix not found."
        )

    return result