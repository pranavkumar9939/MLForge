from fastapi import APIRouter
from pathlib import Path

router = APIRouter(
    prefix = "/datasets",
    tags = ["Datasets"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SAVED_MODELS = BASE_DIR / "saved_models"

@router.get("/")
def get_datasets():

    if not SAVED_MODELS.exists():
        return []

    datasets = [
        folder.name
        for folder in SAVED_MODELS.iterdir()
        if folder.is_dir()
    ]

    datasets.sort()

    return datasets
