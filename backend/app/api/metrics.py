from fastapi import APIRouter, Depends, HTTPException

from app.services.metrics.metrics_service import get_metrics
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/{dataset_name}/{model_name}")
def metrics(dataset_name: str, model_name: str, current_user: User = Depends(get_current_user)):
    require_owner(dataset_name, current_user.id)

    result = get_metrics(dataset_name, model_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Metrics not found")

    return result
