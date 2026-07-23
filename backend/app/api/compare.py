from fastapi import APIRouter, HTTPException

from app.services.comparison.comparison_service import compare_models

router = APIRouter(
    prefix = "/compare",
    tags = ["Model Comparison"]
)

@router.get("/{dataset_name}")
def compare_dataset_models(dataset_name: str):

    result = compare_models(dataset_name)

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Dataset '{dataset_name}' not found."
        )

    return result