from fastapi import APIRouter, Depends, HTTPException

from app.services.comparison.leaderboard_services import built_leaderboard
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/{dataset_name}")
def leaderboard(dataset_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = built_leaderboard(dataset_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return result
