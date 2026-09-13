import io

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User
from app.services.persistence.model_loader import load_saved_model
from app.services.preprocessing.datetime_features import expand_datetime_column

router = APIRouter(prefix="/predict", tags=["Predict"])


def _read_batch_file(file: UploadFile, contents: bytes) -> pd.DataFrame:
    name = (file.filename or "").lower()
    try:
        if name.endswith(".xlsx") or name.endswith(".xls"):
            return pd.read_excel(io.BytesIO(contents))
        return pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be read. Please make sure it's a valid CSV or Excel file.",
        ) from exc


@router.post("/{dataset_name}/{model_name}/batch")
async def predict_batch(
    dataset_name: str,
    model_name: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Run the trained model over every row of an uploaded CSV/Excel file and
    return a CSV with a `prediction` column (and, for classification,
    a `confidence` column) appended.

    Per-row SHAP explanations are intentionally skipped here for
    performance - they're only computed for single predictions
    (POST /predict/{dataset_name}/{model_name}), where the cost is paid
    once instead of once per row.
    """
    require_owner(dataset_name, current_user.id)

    try:
        artifacts = load_saved_model(
            dataset_name=dataset_name,
            model_name=model_name,
            version="production",
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"No trained model named '{model_name}' was found for dataset '{dataset_name}'.",
        )

    contents = await file.read()
    input_df = _read_batch_file(file, contents)

    if len(input_df) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file has no rows.")

    if len(input_df) > settings.MAX_BATCH_PREDICTION_ROWS:
        raise HTTPException(
            status_code=400,
            detail=f"This file has {len(input_df)} rows, which is more than the "
                   f"{settings.MAX_BATCH_PREDICTION_ROWS}-row limit for a single batch prediction. "
                   f"Please split it into smaller files.",
        )

    metadata = artifacts["metadata"]
    input_schema = metadata.get("input_schema", [])

    required_columns = [f["name"] for f in input_schema]
    missing = [c for c in required_columns if c not in input_df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"The uploaded file is missing required column(s): {', '.join(missing)}.",
        )

    working_df = input_df.copy()

    for field in input_schema:
        if field.get("type") == "Datetime" and field["name"] in working_df.columns:
            working_df, _ = expand_datetime_column(working_df, field["name"])

    try:
        X = artifacts["pipeline"].transform(working_df)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="One or more rows don't match what this model expects. "
                   "Please check that every required column has a valid value in every row.",
        ) from exc

    model = artifacts["model"]
    label_encoder = artifacts["label_encoder"]

    raw_predictions = model.predict(X)
    raw_predictions = np.asarray(raw_predictions).reshape(-1)

    output_df = input_df.copy()

    if label_encoder is not None:
        output_df["prediction"] = label_encoder.inverse_transform(raw_predictions)
    else:
        output_df["prediction"] = raw_predictions

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)
        output_df["confidence"] = np.max(probabilities, axis=1)

    csv_buffer = io.StringIO()
    output_df.to_csv(csv_buffer, index=False)
    csv_bytes = io.BytesIO(csv_buffer.getvalue().encode("utf-8"))

    display_name = metadata.get("display_name", dataset_name)
    safe_model = model_name.replace(" ", "_")
    filename = f"{display_name}_{safe_model}_predictions.csv"

    return StreamingResponse(
        csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
