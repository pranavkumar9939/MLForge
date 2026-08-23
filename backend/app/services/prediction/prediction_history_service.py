import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = BASE_DIR / "saved_models"

def get_history_path(
    dataset_name,
    model_name,
    version
):

    model_folder = (
        MODEL_DIR
        / dataset_name
        / model_name
        / version
    )

    model_folder.mkdir(
        parents = True,
        exist_ok = True
    )

    return model_folder / "prediction_history.json"


def load_prediction_history(
    dataset_name,
    model_name,
    version
):

    history_path = get_history_path(
        dataset_name,
        model_name,
        version
    )

    if not history_path.exists():

        return []

    try:

        with open(history_path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):

            return []

        return data

    except json.JSONDecodeError:

        return []



def save_prediction_history(
    dataset_name,
    model_name,
    version,
    input_data,
    prediction,
    confidence,
    explanation = None,
    shap = None
):

    history = load_prediction_history(
        dataset_name,
        model_name,
        version
    )

    next_id = len(history) + 1

    history_record = {
        "id": next_id,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "dataset_name": dataset_name,
        "model_name": model_name,
        "version": version,
        "input": input_data,
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation,
        "shap": shap
    }

    history.append(history_record)

    history_path = get_history_path(
        dataset_name,
        model_name,
        version
    )

    with open(history_path, "w", encoding="utf-8") as f:
         json.dump(
             history,
             f,
             indent=4,
             default=str
         )

    return history_record