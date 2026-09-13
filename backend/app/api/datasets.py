from fastapi import APIRouter, Depends
from pathlib import Path

from app.core.deps import get_current_user
from app.core.ownership import owner_prefix
from app.database.models import User

router = APIRouter(prefix="/datasets", tags=["Datasets"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SAVED_MODELS = BASE_DIR / "saved_models"


@router.get("/")
def get_datasets(current_user: User = Depends(get_current_user)):
    if not SAVED_MODELS.exists():
        return []

    prefix = owner_prefix(current_user.id)

    datasets = [
        folder.name
        for folder in SAVED_MODELS.iterdir()
        if folder.is_dir() and folder.name.startswith(prefix)
    ]
    datasets.sort()
    return datasets
