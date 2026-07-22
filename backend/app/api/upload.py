from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from app.services.dataset_service import analyze_dataset

import pandas as pd
import numpy as np

# from app.services.dataset_service import analyze_dataset
from app.services.preprocessing.preprocessing_service import preprocess_dataset
from app.services.model_training.trainer import train_model
from app.services.model_training.evaluator import evaluate_model

from app.services.persistence.model_saver import save_model

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
        pipeline = preprocessing_result["pipeline"],
        feature_names = preprocessing_result["summary"]["numerical_columns"],
        label_encoder = preprocessing_result.get("label_encoder")
    )

    evaluation = evaluate_model(training_result)

    best_model_name = evaluation["best_model"]["model_name"]

    best_model = None

    for trained_model in training_result["trained_models"]:

        if trained_model["model_name"] == best_model_name:

            best_model = trained_model
            break


    if best_model is not None:

        if analysis["problem_type"] == "Regression":
            performance = evaluation["best_model"]["r2_score"]

        else:
            performance = evaluation["best_model"]["accuracy"]["value"]

        X_train = training_result["X_train"]

        rng = np.random.default_rng(seed=42)

        sample_size = min(100, len(X_train))

        indices = rng.choice(
            len(X_train),
            size = sample_size,
            replace=False
        )

        save_model(
            model = best_model["model"],
            pipeline = preprocessing_result["pipeline"],
            label_encoder = preprocessing_result.get("label_encoder"),
            feature_names = preprocessing_result["feature_names"].tolist(),
            metadata = {
                "model_name": best_model_name,
                "problem_type": analysis["problem_type"],
                "algorithm": type(best_model["model"]).__name__,
                "target_column": analysis["target_column"],
                "feature_count": len(preprocessing_result["feature_names"]),
                "dataset_name": file.filename.replace(".csv",""),
                "performance": performance,
                "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mlforge_version": "1.0.0"
            },
            dataset_name = file.filename.replace(".csv",""),
            model_name = best_model["model_name"],
            evaluation = evaluation["best_model"],
            background_data = X_train[indices]
        )

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