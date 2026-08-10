import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

def get_tuning_results( dataset_name, model_name):

    tuning_file = os.path.join(
        MODEL_DIR,
        dataset_name,
        model_name,
        "hyperparameter_tuning.json"
    )

    if not os.path.exists(tuning_file):

        return None

    with open(tuning_file, "r") as f:

        return json.load(f)