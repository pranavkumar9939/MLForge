from fastapi import APIRouter, Depends, HTTPException

from app.services.hyperparameter.tuning_service import get_tuning_results
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/tuning", tags=["Hyperparameter Tuning"])


@router.get("/{dataset_name}/{model_name}")
def tuning_results(dataset_name: str, model_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = get_tuning_results(dataset_name, model_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Tuning results not found")

    return result
