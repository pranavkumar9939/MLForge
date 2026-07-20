import pandas as pd

from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest
from app.services.persistence.model_loader import load_saved_model

router = APIRouter(prefix = "/predict", tags = ["Predict"])

@router.post("/")
def get_prediction(request: PredictionRequest):

    artifacts = load_saved_model()

    input_df = pd.DataFrame([request.features])

    X = artifacts["pipeline"].transform(input_df)
    prediction = artifacts["model"].predict(X)[0]

    if artifacts["label_encoder"] is not None:
        prediction = artifacts["label_encoder"].inverse_transform([prediction])[0]

    

    return {
        "prediction": prediction
    }