from fastapi import APIRouter, Depends, HTTPException

from app.services.persistence.model_registry import list_saved_models, get_model_details, get_model_evaluation
from app.core.deps import get_current_user
from app.core.ownership import owner_prefix, require_owner
from app.database.models import User

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/")
def get_saved_models(current_user: User = Depends(get_current_user)):
    """
    List only the datasets/models belonging to the authenticated user.
    """
    all_data = list_saved_models()
    prefix = owner_prefix(current_user.id)

    own_datasets = [
        dataset for dataset in all_data["datasets"]
        if dataset["dataset_name"].startswith(prefix)
    ]

    return {"datasets": own_datasets}


@router.get("/{dataset_name}/{model_name}")
def get_model(
    dataset_name: str,
    model_name: str,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)

    metadata = get_model_details(dataset_name, model_name)

    if metadata is None:
        raise HTTPException(status_code=404, detail="Model not found")

    return metadata


@router.get("/{dataset_name}/{model_name}/evaluation")
def get_evaluation(
    dataset_name: str,
    model_name: str,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)

    evaluation = get_model_evaluation(dataset_name, model_name)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return evaluation
