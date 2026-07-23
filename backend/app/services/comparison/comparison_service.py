from pathlib import Path
import json
import os 

BASE_DIR = Path(__file__).resolve().parents[3]

BASE_MODEL_DIR = BASE_DIR / "saved_models"

def compare_models(dataset_name: str):

    dataset_path = BASE_MODEL_DIR / dataset_name
    if not dataset_path.exists():
        return None

    models = []

    problem_type = None

    for model_folder in dataset_path.iterdir():

        if not model_folder.is_dir():
            continue

        evaluation_file = model_folder / "evaluation.json"
        metadata_file = model_folder / "metadata.json"

        if not evaluation_file.exists():
            continue

        with open(evaluation_file) as f:
            evaluation = json.load(f)

        with open(metadata_file) as f:
            metadata = json.load(f)

        if problem_type is None:
            problem_type = metadata["problem_type"]

        model_result =  {
            "model_name": metadata["model_name"],
            "accuracy": evaluation["accuracy"]["value"],
            "precision": evaluation["precision"]["value"],
            "recall": evaluation["recall"]["value"],
            "f1_score": evaluation["f1_score"]["value"],

            "overall_score": evaluation["overall_assessment"]["overall_score"],
            "status": evaluation["overall_assessment"]["status"],
            "color": evaluation["accuracy"]["color"]
        }

        models.append(model_result)

    models.sort(
        key = lambda x: x["overall_score"],
        reverse = True
    )

    best_model = models[0]["model_name"] if models else None

    return {
        "dataset": dataset_name,
        "problem_type": problem_type,
        "best_model": best_model,
        "models": models
    }