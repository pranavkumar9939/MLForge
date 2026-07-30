from fastapi import APIRouter, HTTPException
from app.services.metrics.metrics_service import get_metrics

router = APIRouter(
    prefix = "/metrics",
    tags = ["Metrics"]
)

@router.get("/{dataset_name}/{model_name}")
def metrics(
    dataset_name: str,
    model_name: str
):

    result = get_metrics(
        dataset_name,
        model_name
    )

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail="Metrics not found"
        )

    return result