from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.prediction.prediction_history_service import (
    get_prediction_history_paginated,
    get_prediction_by_id,
    get_prediction_statistics,
)
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/prediction-history", tags=["Prediction History"])


@router.get("/{dataset_name}/{model_name}/{version}")
def get_history(
    dataset_name: str,
    model_name: str,
    version: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)
    return get_prediction_history_paginated(
        dataset_name=dataset_name, model_name=model_name, version=version, limit=limit, offset=offset
    )


@router.get("/{dataset_name}/{model_name}/{version}/stats")
def get_statistics(
    dataset_name: str,
    model_name: str,
    version: str,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)
    return get_prediction_statistics(dataset_name=dataset_name, model_name=model_name, version=version)


@router.get("/{dataset_name}/{model_name}/{version}/prediction/{prediction_id}")
def get_single_prediction(
    dataset_name: str,
    model_name: str,
    version: str,
    prediction_id: int,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)
    prediction = get_prediction_by_id(
        dataset_name=dataset_name, model_name=model_name, version=version, prediction_id=prediction_id
    )
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
