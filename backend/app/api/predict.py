from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest

router = APIRouter(prefix = "/predict", tags = ["Predict"])

@router.post("/")
def get_prediction(request: PredictionRequest):

    return request