import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = BASE_DIR / "saved_models"


def _registry_path(
    dataset_name,
    model_name
):

    model_folder = MODEL_DIR / dataset_name / model_name

    model_folder.mkdir(
        parents = True,
        exist_ok = True
    )

    return model_folder / "registry.json"


def load_registry(
    dataset_name,
    model_name
):

    registry_file = _registry_path(
        dataset_name,
        model_name
    )

    if not registry_file.exists():

        return {
            "production": None,
            "versions": []
        }

    with open(registry_file, "r") as f:

        return json.load(f)



def save_registry(
    dataset_name,
    model_name,
    registry_data
):

    registry_file = _registry_path(
        dataset_name,
        model_name
    )

    with open(registry_file, "w") as f:

        json.dump(
            registry_data,
            f,
            indent = 4
        )


def register_model_version(
    dataset_name,
    model_name,
    version,
    score
):

    registry = load_registry(
        dataset_name,
        model_name
    )

    registry["versions"].append({

        "version": version,
        "score": score
    })

    if registry["production"] is None:

        registry["production"] = version

    save_registry(
        dataset_name,
        model_name,
        registry
    )



def get_model_versions(
    dataset_name,
    model_name
):

    return load_registry(
        dataset_name,
        model_name
    )


def set_production_model(
    dataset_name,
    model_name,
    version
):

    registry = load_registry(
        dataset_name,
        model_name
    )

    versions = [
        v["version"] for v in registry["versions"]
    ]

    if version not in versions:

        raise ValueError(
            f"{version} not found"
        )

    registry["production"] = version

    save_registry(
        dataset_name,
        model_name,
        registry
    )

    return registry