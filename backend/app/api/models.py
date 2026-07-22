from fastapi import APIRouter, HTTPException

from app.services.persistence.model_registry import list_saved_models, get_model_details, get_model_evaluation

router = APIRouter(
    prefix = "/models",
    tags = ["Models"]
)

@router.get("/")
def get_saved_models():

    return list_saved_models()


@router.get("/{dataset_name}/{nodel_name}")
def get_model(
    dataset_name: str,
    model_name: str
):

    metadata = get_model_details(
        dataset_name,
        model_name
    )

    if metadata is None:

        raise HTTPException(
            status_code = 404,
            detail = "Model not found"
        )

    return metadata


@router.get("/{dataset_name}/{model_name}/evaluation")
def get_evaluation(
    dataset_name: str,
    model_name: str
):

    evaluation = get_model_evaluation(
        dataset_name,
        model_name
    )

    if evaluation is None:
        raise HTTPException(
            status_code = 404,
            detail = "Evaluation not found"
        )

    return evaluation