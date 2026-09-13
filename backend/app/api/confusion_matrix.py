from fastapi import APIRouter, Depends, HTTPException

from app.services.evaluation.confusion_matrix_service import get_confusion_matrix
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter()


@router.get("/{dataset_name}/{model_name}")
def confusion_matrix(dataset_name: str, model_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = get_confusion_matrix(dataset_name, model_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Confusion Matrix not found.")

    return result
