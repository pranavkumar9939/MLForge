from fastapi import APIRouter, Depends, HTTPException

from app.services.comparison.comparison_service import compare_models
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/compare", tags=["Model Comparison"])


@router.get("/{dataset_name}")
def compare_dataset_models(dataset_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = compare_models(dataset_name)

    if result is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found.")

    return result
