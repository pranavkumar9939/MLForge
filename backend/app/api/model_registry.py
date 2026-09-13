from fastapi import APIRouter, Depends, HTTPException

from app.services.model_registry.registry_service import get_model_versions, set_production_model
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/registry", tags=["Model registry"])


@router.get("/{dataset_name}/{model_name}")
def versions(dataset_name: str, model_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)
    try:
        return get_model_versions(dataset_name, model_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{dataset_name}/{model_name}/{version}")
def make_production(
    dataset_name: str,
    model_name: str,
    version: str,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)
    try:
        return set_production_model(dataset_name, model_name, version)
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e))
