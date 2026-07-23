from app.services.persistence.model_loader  import load_saved_model

def get_roc_curve(
        dataset_name,
        model_name
):

    artifacts = load_saved_model(
        dataset_name,
        model_name
    )

    return {
        "dataset": dataset_name,
        "model": model_name,
        "roc_curve": artifacts["roc_curve"]
    }