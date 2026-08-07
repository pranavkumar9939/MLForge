from fastapi import APIRouter, HTTPException

from app.services.comparison.leaderboard_services import built_leaderboard

router = APIRouter(
    prefix = "/leaderboard",
    tags = ["Leaderboard"]
)

@router.get("/{dataset_name}")
def leaderboard(dataset_name: str):

    result = built_leaderboard(dataset_name)

    if result is None:

        raise HTTPException(
            status_code = 404,
            detail = "Dataset not found"
        )

    return result