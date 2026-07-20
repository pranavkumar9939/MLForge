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

os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(
        model,
        pipeline,
        label_encoder,
        feature_names,
        metadata
):
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_path = os.path.join(MODEL_DIR, "model.pkl")
    pipeline_path = os.path.join(MODEL_DIR, "pipeline.pkl")
    label_encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
    feature_names_path = os.path.join(MODEL_DIR, "feature_names.json")
    metadata_path = os.path.join(MODEL_DIR, "metadata.json")

    joblib.dump(model, model_path)
    joblib.dump(pipeline, pipeline_path)

    if label_encoder is not None:
        joblib.dump(label_encoder, label_encoder_path)

    with open(feature_names_path, "w") as f:
        json.dump(feature_names, f, indent=4)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

