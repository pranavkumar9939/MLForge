import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.prediction import PredictionRequest
from app.services.persistence.model_loader import load_saved_model
from app.services.prediction.prediction_service import predict_single_sample
from app.services.prediction.prediction_history_service import save_prediction_history
from app.services.preprocessing.datetime_features import expand_datetime_column
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User

router = APIRouter(prefix="/predict", tags=["Predict"])


@router.post("/{dataset_name}/{model_name}")
def get_prediction(
    dataset_name: str,
    model_name: str,
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
):
    require_owner(dataset_name, current_user.id)

    try:
        artifacts = load_saved_model(
            dataset_name=dataset_name,
            model_name=model_name,
            version="production"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"No trained model named '{model_name}' was found for dataset '{dataset_name}'.",
        )

    model_version = artifacts["metadata"].get("version") or artifacts["metadata"].get("model_version")

    if model_version is None:
        raise HTTPException(
            status_code=500,
            detail="This model's metadata is missing a version and cannot be used for prediction.",
        )

    input_df = pd.DataFrame([request.features])

    # If the model was trained on datetime-derived features (year/month/day/
    # etc.), the raw date submitted by the caller needs to be expanded the
    # same way before the pipeline can transform it. The pipeline selects
    # its expected columns by name, so any extra/raw columns here are
    # harmless - only the derived ones actually get used.
    input_schema = artifacts["metadata"].get("input_schema", [])
    for field in input_schema:
        if field.get("type") == "Datetime" and field["name"] in input_df.columns:
            input_df, _ = expand_datetime_column(input_df, field["name"])

    try:
        X = artifacts["pipeline"].transform(input_df)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The submitted values don't match what this model expects. "
                   "Please check that every required field is filled in correctly.",
        ) from exc

    result = predict_single_sample(
        model=artifacts["model"],
        model_name=artifacts["metadata"]["model_name"],
        input_data=X,
        feature_names=artifacts["feature_names"],
        background_data=artifacts["background_data"],
        label_encoder=artifacts["label_encoder"]
    )

    history_record = save_prediction_history(
        dataset_name=dataset_name,
        model_name=model_name,
        version=model_version,
        input_data=request.features,
        prediction=result["prediction"],
        confidence=result["confidence"],
        explanation=result.get("explanation"),
        shap=result.get("shap")
    )

    return {
        "dataset_name": dataset_name,
        "model_name": model_name,
        "version": model_version,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "explanation": result["explanation"],
        "shap": result["shap"],
        "history_id": history_record["id"]
    }
