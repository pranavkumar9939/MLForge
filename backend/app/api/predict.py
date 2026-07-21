import pandas as pd

from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest
from app.services.persistence.model_loader import load_saved_model
from app.services.prediction.prediction_service import predict_single_sample

router = APIRouter(prefix = "/predict", tags = ["Predict"])

@router.post("/{dataset_name}/{model_name}")
def get_prediction(dataset_name: str,
    model_name: str,
    request: PredictionRequest
):

    artifacts = load_saved_model(
        dataset_name=dataset_name,
        model_name=model_name
    )

    input_df = pd.DataFrame([request.features])

    X = artifacts["pipeline"].transform(input_df)
    
    result = predict_single_sample(
        model = artifacts["model"],
        model_name = artifacts["metadata"]["model_name"],
        input_data = X,
        feature_names = artifacts["feature_names"],
        label_encoder = artifacts["label_encoder"]
    )

    return result