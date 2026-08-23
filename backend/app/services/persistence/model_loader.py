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
        model_name,
        version = None
):

    dataset_folder = os.path.join(MODEL_DIR, dataset_name)

    if version == "production":

        version = get_production_version(
            dataset_name,
            model_name
        )

    if version is not None:

        model_folder = os.path.join(dataset_folder, model_name,version)

    else:

        model_folder = get_latest_version_folder(dataset_folder, model_name)

    if not os.path.exists(model_folder):
        raise FileNotFoundError(
            f"Model '{model_name}' for dataset '{dataset_name}' not found."
        )

    model_path = os.path.join(model_folder, "model.pkl")
    pipeline_path = os.path.join(model_folder, "pipeline.pkl")
    label_encoder_path = os.path.join(model_folder, "label_encoder.pkl")
    feature_names_path = os.path.join(model_folder, "feature_names.json")
    metadata_path = os.path.join(model_folder, "metadata.json")
    background_data_path = os.path.join(model_folder, "background_data.pkl")
    roc_curve_path = os.path.join(model_folder, "roc_curve.json")
    confusion_matrix_path = os.path.join(model_folder, "confusion_matrix.json")
    evaluation_path = os.path.join(model_folder, "evaluation.json")
    hyperparameter_tuning_path = os.path.join(model_folder, "hyperparameter_tuning.json")

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)

    label_encoder = None
    if os.path.exists(label_encoder_path):
        label_encoder = joblib.load(label_encoder_path)

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(roc_curve_path, "r") as f:
        roc_curve = json.load(f)

    with open(confusion_matrix_path, "r") as f:
        confusion_matrix = json.load(f)

    with open(evaluation_path, "r") as f:
        evaluation = json.load(f)

    background_data = None

    if os.path.exists(background_data_path):
        background_data = joblib.load(background_data_path)

    hyperparameter_tuning = {}

    with open(hyperparameter_tuning_path, "r") as f:
        hyperparameter_tuning = json.load(f)


    return {
        "model": model,
        "pipeline": pipeline,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "metadata": metadata,
        "background_data": background_data,
        "roc_curve": roc_curve,
        "confusion_matrix": confusion_matrix,
        "evaluation": evaluation,
        "hyperparameter_tuning": hyperparameter_tuning,
        "version": version
    }


def get_latest_version_folder(
    dataset_folder,
    model_name
):

    model_folder = os.path.join(
        dataset_folder,
        model_name
    )

    registry_path = os.path.join(model_folder, "registry.json")

    if not os.path.exists(registry_path):

        raise FileNotFoundError(
            f"Registry not found for "
            f"{model_name}"
        )

    with open(registry_path, "r") as f:

        registry = json.load(f)

    if not registry["versions"]:
        raise FileNotFoundError(
            f"No model versions found for "
            f"{model_name}"
        )

    latest_version = registry["versions"][-1]["version"]

    return os.path.join(
        model_folder,
        latest_version
    )


def get_production_version(
    dataset_name,
    model_name
):

    model_folder = os.path.join(
        MODEL_DIR,
        dataset_name,
        model_name
    )

    registry_path = os.path.join(
        model_folder,
        "registry.json"
    )

    if not os.path.exists(registry_path):
        raise FileNotFoundError(
            f"Registry not found for "
            f"{dataset_name}/{model_name}"
        )

    with open(registry_path, "r") as f:
        registry = json.load(f)

    production_version = registry.get("production")

    if production_version is None:

        raise FileNotFoundError(
            f"No production model configured "
            f"for {dataset_name}/{model_name}"
        )

    return production_version