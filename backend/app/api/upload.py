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

from app.services.model_registry.registry_service import load_registry, register_model_version

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

    # best_model_name = evaluation["best_model"]["model_name"]

    # best_model = None

    for trained_model in training_result["trained_models"]:

        model_name = trained_model["model_name"]

        dataset_name = file.filename.replace(".csv", "")

        registry = load_registry(
            dataset_name,
            model_name
        )

        existing_versions = registry["versions"]

        version_number = len(existing_versions) + 1
        version = f"v{version_number}"

        model_eval = None

        for result in evaluation["all_models"]:

            if result["model_name"] == model_name:

                model_eval = result
                break

        if model_eval is None:
            continue

        if analysis["problem_type"] == "Regression":
            performance = model_eval["r2_score"]

        else:
            performance = model_eval["accuracy"]["value"]

        X_train = training_result["X_train"]

        rng = np.random.default_rng(seed = 42)

        sample_size = min(100, len(X_train))

        indices = rng.choice(
            len(X_train),
            size = sample_size,
            replace = False
        )

        save_model(
            model = trained_model["model"],
            pipeline = preprocessing_result["pipeline"],
            label_encoder = preprocessing_result.get("label_encoder"),
            feature_names = preprocessing_result["feature_names"].tolist(),

            metadata = {
                "model_name": model_name,
                "problem_type": analysis["problem_type"],
                "algorithm": type(trained_model["model"]).__name__,
                "target_column": analysis["target_column"],
                "feature_count": len(preprocessing_result["feature_names"]),
                "dataset_name": file.filename.replace(".csv", ""),
                "performance": performance,
                "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mlforge_version": "1.0.0"
            },

            dataset_name = file.filename.replace(".csv", ""),
            model_name = model_name,
            evaluation = model_eval,
            background_data = X_train[indices],

            roc_curve = trained_model["roc_curve"],
            confusion_matrix = trained_model["confusion_matrix"],
            tuned = trained_model["tuned"],
            best_params = trained_model["best_params"],
            best_cv_score = trained_model["best_cv_score"]
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