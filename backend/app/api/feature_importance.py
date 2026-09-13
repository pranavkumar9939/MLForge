from fastapi import APIRouter, Depends, HTTPException

from app.services.feature_importance.feature_importance_service import get_feature_importance
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/feature-importance", tags=["Feature Importance"])


@router.get("/{dataset_name}/{model_name}")
def feature_importance(
    dataset_name: str,
    model_name: str,
    top_n: int = 10,
    current_user: User = Depends(get_current_user),
):
    """
    Return the top N most important features for a trained model.
    """
    require_owner(dataset_name, current_user.id)

    result = get_feature_importance(dataset_name=dataset_name, model_name=model_name, top_n=top_n)

    if result is None:
        raise HTTPException(status_code=404, detail="Dataset or model not found.")

    return result
