from fastapi import APIRouter, HTTPException

from app.services.hyperparameter.tuning_service import get_tuning_results

router = APIRouter(
    prefix = "/tuning",
    tags = ["Hyperparameter Tuning"]
)

@router.get("/{dataset_name}/{model_name}")

def tuning_results(
    dataset_name: str,
    model_name: str
):

    result = get_tuning_results(
        dataset_name,
        model_name
    )

    if result is None:

        raise HTTPException(
            status_code = 404,
            detail = "Tuning results not found"
        )

    return result