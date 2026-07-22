import os
import json

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

def list_saved_models():
    """
    Scan teh saved_models folder and return all available
    datasets and their trained models.
    """

    print("MODEL_DIR =", MODEL_DIR)
    print("Exists =", os.path.exists(MODEL_DIR))

    if not os.path.exists(MODEL_DIR):
        return {
            "datasets": []
        }

    datasets = []

    for dataset_name in os.listdir(MODEL_DIR):

        dataset_path = os.path.join(
            MODEL_DIR,
            dataset_name
        )

        # Ignores files
        if not os.path.isdir(dataset_path):
            continue

        models = []

        for model_name in os.listdir(dataset_path):

            model_path = os.path.join(
                dataset_path,
                model_name
            )

            if not os.path.isdir(model_path):
                continue

            metadata_path = os.path.join(
                    model_path,
                    "metadata.json"
                )

            metadata = {}

            if os.path.exists(metadata_path):

                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

            models.append({
                "model_name": metadata.get("model_name", model_name),
                "problem_type": metadata.get("problem_type"),
                "target_column": metadata.get("target_column"),
                "dataset_name": metadata.get("dataset_name"),
                "performance": metadata.get("performance"),
                "training_date": metadata.get("training_date")
            })

            

        datasets.append({
            "dataset_name": dataset_name,
            "models": models
        })

    return {
        "datasets": datasets
    }



def get_model_details(
        dataset_name,
        model_name
):

    model_path = os.path.join(
        MODEL_DIR,
        dataset_name,
        model_name
    )

    if not os.path.exists(model_path):
        return None

    metadata_path = os.path.join(
        model_path,
        "metadata.json"
    )

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return metadata


def get_model_evaluation(
        dataset_name,
        model_name
):

    model_path = os.path.join(
        MODEL_DIR,
        dataset_name,
        model_name
    )

    if not os.path.exists(model_path):
        return None

    evaluation_path = os.path.join(
        model_path,
        "evaluation.json"
    )

    with open(evaluation_path, "r") as f:
        evaluation = json.load(f)

    return evaluation
