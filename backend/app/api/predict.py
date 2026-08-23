import pandas as pd

from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest
from app.services.persistence.model_loader import load_saved_model
from app.services.prediction.prediction_service import predict_single_sample
from app.services.prediction.prediction_history_service import save_prediction_history

router = APIRouter(prefix = "/predict", tags = ["Predict"])

@router.post("/{dataset_name}/{model_name}")
def get_prediction(
    dataset_name: str,
    model_name: str,
    request: PredictionRequest
):

    artifacts = load_saved_model(
        dataset_name=dataset_name,
        model_name=model_name,
        version = "production"
    )

    model_version = artifacts["metadata"].get("version")

    if model_version is None:

        model_version = artifacts["metadata"].get("model_version")

    if model_version is None:

        raise ValueError(
            "Model version not found in metadata"
        )

    input_df = pd.DataFrame([request.features])

    X = artifacts["pipeline"].transform(input_df)
    
    result = predict_single_sample(
        model = artifacts["model"],
        model_name = artifacts["metadata"]["model_name"],
        input_data = X,
        feature_names = artifacts["feature_names"],
        background_data = artifacts["background_data"],
        label_encoder = artifacts["label_encoder"]
    )

    history_record = save_prediction_history(
        dataset_name=dataset_name,
        model_name=model_name,
        version=model_version,
        input_data=request.features,
        prediction=result["prediction"],
        confidence=result["confidence"],
        explanation=result.get("explanation"),
        shap = result.get("shap")
    )

    return {
        "dataset_name": dataset_name,

        "model_name": model_name,

        "version": artifacts["version"],

        "prediction": result["prediction"],

        "confidence": result["confidence"],

        "explanation": result["explanation"],

        "shap": result["shap"],

        "history_id": history_record["id"]
    }