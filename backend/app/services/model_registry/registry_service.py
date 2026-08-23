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

    if "versions" not in registry:
        registry["versions"] = []

    if "production" not in registry:
        registry["production"] = None

    existing_versions = []

    for item in registry["versions"]:

        if isinstance(item, dict):

            existing_versions.append(
                item.get("version")
            )

        elif isinstance(item, str):

            existing_versions.append(item)

    if version not in existing_versions:

        registry["versions"].append({
            "version": version,
            "score": score
        })

    # First model version becomes production
    if registry["production"] is None:

        registry["production"] = version

    save_registry(
        dataset_name,
        model_name,
        registry
    )

    return registry



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

    versions = registry.get("versions", [])

    found = False

    for item in versions:

        # New registry format
        if isinstance(item, dict):

            if item.get("version") == version:
                found = True
                break

        # Old registry format
        elif isinstance(item, str):

            if item == version:
                found = True
                break

    if not found:

        raise ValueError(
            f"Version '{version}' not found "
            f"for dataset '{dataset_name}' "
            f"and model '{model_name}'"
        )

    registry["production"] = version

    save_registry(
        dataset_name,
        model_name,
        registry
    )

    return {
        "message": "Production model updated successfully",
        "dataset_name": dataset_name,
        "model_name": model_name,
        "production": version,
        "registry": registry
    }