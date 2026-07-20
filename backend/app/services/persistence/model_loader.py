import joblib
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


def load_saved_model():

    model_path = os.path.join(MODEL_DIR, "model.pkl")
    pipeline_path = os.path.join(MODEL_DIR, "pipeline.pkl")
    label_encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
    feature_names_path = os.path.join(MODEL_DIR, "feature_names.json")
    metadata_path = os.path.join(MODEL_DIR, "metadata.json")

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)

    label_encoder = None
    if os.path.exists(label_encoder_path):
        label_encoder = joblib.load(label_encoder_path)

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)


    return {
        "model": model,
        "pipeline": pipeline,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "metadata": metadata
    }