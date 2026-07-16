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

    df = pd.read_csv(file_path)

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    analysis = analyze_dataset(file_path)

    preprocessing_result = preprocess_dataset(
        df,
        analysis
    )

    training_result = train_model(
        preprocessing_result["X"],
        preprocessing_result["y"],
        analysis
    )

    evaluation = evaluate_model(training_result)

    return {
        "filename": file.filename,
        "message": "File Uploaded successfully",
        "analysis": analysis,
        "preprocessing": preprocessing_result["summary"],
        "trainig": {
            "model_name": training_result["model_name"],
            "problem_type": training_result["problem_type"]
        },
        "evaluation": evaluation
    }