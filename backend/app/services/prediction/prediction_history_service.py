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


def get_prediction_history_paginated(
    dataset_name,
    model_name,
    version,
    limit=20,
    offset=0
):

    history = load_prediction_history(
        dataset_name,
        model_name,
        version
    )

    total = len(history)

    paginated_history = history[
        offset: offset + limit
    ]

    return {
        "dataset_name": dataset_name,
        "model_name": model_name,
        "version": version,
        "total": total,
        "limit": limit,
        "offset": offset,
        "count": len(paginated_history),
        "history": paginated_history
    }


def get_prediction_by_id(
    dataset_name,
    model_name,
    version,
    prediction_id
):

    history = load_prediction_history(
        dataset_name,
        model_name,
        version
    )

    for record in history:

        if record["id"] == prediction_id:

            return record

    return None


def get_prediction_statistics(
    dataset_name,
    model_name,
    version
):

    history = load_prediction_history(
        dataset_name,
        model_name,
        version
    )

    total_predictions = len(history)

    if total_predictions == 0:

        return {
            "dataset_name": dataset_name,
            "model_name": model_name,
            "version": version,
            "total_predictions": 0,
            "average_confidence": None,
            "latest_prediction": None
        }


    confidences = [

        record["confidence"]

        for record in history

        if record.get("confidence") is not None
        and isinstance(
            record.get("confidence"),
            (int, float)
        )
    ]


    average_confidence = None

    if confidences:

        average_confidence = sum(
            confidences
        ) / len(confidences)


    latest_prediction = history[-1]


    return {

        "dataset_name": dataset_name,

        "model_name": model_name,

        "version": version,

        "total_predictions": total_predictions,

        "average_confidence": average_confidence,

        "latest_prediction": {

            "id": latest_prediction["id"],

            "timestamp": latest_prediction[
                "timestamp"
            ],

            "prediction": latest_prediction[
                "prediction"
            ],

            "confidence": latest_prediction.get(
                "confidence"
            )
        }
    }