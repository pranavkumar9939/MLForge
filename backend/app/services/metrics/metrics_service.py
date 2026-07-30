from app.services.persistence.model_loader import load_saved_model

def get_metrics(
        dataset_name,
        model_name
):

    artifacts = load_saved_model(
        dataset_name,
        model_name
    )

    evaluation = artifacts["evaluation"]

    return {
        "dataset": dataset_name,
        "model": model_name,

        "accuracy": evaluation.get("accuracy", {}).get("value", 0),
        "precision": evaluation.get("precision", {}).get("value", 0),
        "recall": evaluation.get("recall", {}).get("value", 0),
        "f1_score": evaluation.get("f1_score", {}).get("value", 0)
    }