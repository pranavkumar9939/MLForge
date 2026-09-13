from fastapi import APIRouter, Depends, HTTPException

from app.services.evaluation.roc_service import get_roc_curve
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter()


@router.get("/{dataset_name}/{model_name}")
def roc(dataset_name: str, model_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = get_roc_curve(dataset_name, model_name)

    if result is None:
        raise HTTPException(status_code=404, detail="ROC curve not found.")

    return result
