import json
import os

from app.services.persistence.model_loader import get_latest_version_folder

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")


def get_tuning_results(dataset_name, model_name):

    dataset_folder = os.path.join(MODEL_DIR, dataset_name)

    try:
        model_folder = get_latest_version_folder(dataset_folder, model_name)
    except FileNotFoundError:
        return None

    tuning_file = os.path.join(model_folder, "hyperparameter_tuning.json")

    if not os.path.exists(tuning_file):
        return None

    with open(tuning_file, "r") as f:
        return json.load(f)
