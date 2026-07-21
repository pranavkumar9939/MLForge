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


def load_saved_model(
        dataset_name,
        model_name
):

    dataset_folder = os.path.join(MODEL_DIR, dataset_name)
    model_folder = os.path.join(dataset_folder, model_name)

    if not os.path.exists(model_folder):
        raise FileNotFoundError(
            f"Model '{model_name}' for dataset '{dataset_name}' not found."
        )

    model_path = os.path.join(model_folder, "model.pkl")
    pipeline_path = os.path.join(model_folder, "pipeline.pkl")
    label_encoder_path = os.path.join(model_folder, "label_encoder.pkl")
    feature_names_path = os.path.join(model_folder, "feature_names.json")
    metadata_path = os.path.join(model_folder, "metadata.json")

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