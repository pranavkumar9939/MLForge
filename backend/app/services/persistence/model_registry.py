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


def _resolve_active_version_folder(model_path):
    """
    Resolve which version subfolder to read metadata/evaluation from.

    Models are saved under `dataset/model_name/{version}/...`. This looks
    up `registry.json` to find the production version, falling back to the
    most recently added version, falling back to legacy flat layout
    (metadata.json directly under model_path) for backwards compatibility
    with models saved by older code.
    """

    registry_path = os.path.join(model_path, "registry.json")

    if os.path.exists(registry_path):
        with open(registry_path, "r") as f:
            registry = json.load(f)

        version = registry.get("production")

        if version is None and registry.get("versions"):
            last = registry["versions"][-1]
            version = last.get("version") if isinstance(last, dict) else last

        if version is not None:
            version_folder = os.path.join(model_path, version)
            if os.path.exists(version_folder):
                return version_folder

    # Legacy fallback: metadata.json directly under model_path
    return model_path


def list_saved_models():
    """
    Scan the saved_models folder and return all available
    datasets and their trained models.
    """

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

            # "clustering" and "dimensionality_reduction" are reserved
            # subfolder names used for unsupervised results (results.json),
            # not versioned supervised models - skip them here.
            if model_name in ("clustering", "dimensionality_reduction"):
                continue

            active_folder = _resolve_active_version_folder(model_path)

            metadata_path = os.path.join(
                active_folder,
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
                "display_name": metadata.get("display_name", metadata.get("dataset_name")),
                "performance": metadata.get("performance"),
                "training_date": metadata.get("training_date"),
                "version": metadata.get("version"),
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

    active_folder = _resolve_active_version_folder(model_path)
    metadata_path = os.path.join(active_folder, "metadata.json")

    if not os.path.exists(metadata_path):
        return None

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    # Encoded (post-preprocessing) feature names, e.g. one-hot expanded
    # columns - useful for SHAP/importance labeling, NOT for building a raw
    # input form (use metadata["input_schema"] for that instead).
    feature_names_path = os.path.join(active_folder, "feature_names.json")
    if os.path.exists(feature_names_path):
        with open(feature_names_path, "r") as f:
            metadata["encoded_feature_names"] = json.load(f)
    else:
        metadata["encoded_feature_names"] = []

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

    active_folder = _resolve_active_version_folder(model_path)
    evaluation_path = os.path.join(active_folder, "evaluation.json")

    if not os.path.exists(evaluation_path):
        return None

    with open(evaluation_path, "r") as f:
        evaluation = json.load(f)

    return evaluation
