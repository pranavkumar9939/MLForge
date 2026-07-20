from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from app.services.dataset_service import analyze_dataset

import pandas as pd

# from app.services.dataset_service import analyze_dataset
from app.services.preprocessing.preprocessing_service import preprocess_dataset
from app.services.model_training.trainer import train_model
from app.services.model_training.evaluator import evaluate_model


router = APIRouter(prefix="/upload", tags=["Upload"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_FOLDER = BASE_DIR/"uploads"

UPLOAD_FOLDER.mkdir(exist_ok=True)

@router.post("/")
async def upload_dataset(file: UploadFile = File(...)):

    file_path = UPLOAD_FOLDER / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("File Exists:",file_path.exists())
    print("File size:", file_path.stat().st_size)

    df = pd.read_csv(file_path)

    print(df.shape)
    print(df.head())

    analysis = analyze_dataset(df)

    preprocessing_result = preprocess_dataset(
        df,
        analysis
    )

    training_result = train_model(
        preprocessing_result["X"],
        preprocessing_result["y"],
        analysis,
        feature_names = preprocessing_result["summary"]["numerical_columns"],
        label_encoder = preprocessing_result.get("label_encoder")
    )

    evaluation = evaluate_model(training_result)

    return {
        "filename": file.filename,
        "message": "File Uploaded successfully",
        "analysis": analysis,
        "preprocessing": preprocessing_result["summary"],
        "trainig": {
            "problem_type": training_result["problem_type"],
            "models_trained": [
                model["model_name"]
                for model in training_result["trained_models"]
            ]
        },
        "evaluation": evaluation
    }