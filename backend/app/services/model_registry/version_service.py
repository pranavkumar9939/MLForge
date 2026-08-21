from .registry_service import load_registry

def generate_version(
    dataset_name,
    model_name
):

    registry = load_registry(
        dataset_name,
        model_name
    )

    count = len(registry["versions"]) + 1

    return f"v{count}"