from fastapi import APIRouter

from app.services.persistence.model_registry import list_saved_models

router = APIRouter(
    prefix = "/models",
    tags = ["Models"]
)

@router.get("/")
def get_saved_models():

    return list_saved_models()