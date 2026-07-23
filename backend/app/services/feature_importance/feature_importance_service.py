from app.services.persistence.model_loader import load_saved_model
from app.services.explainability.feature_importance import generate_feature_importance

def get_feature_importance(
        dataset_name: str,
        model_name: str,
        top_n: int = 10
):
    """
    Load a trained model and return its feature importance.
    """

    artifacts = load_saved_model(
        dataset_name=dataset_name,
        model_name=model_name
    )

    feature_importance = generate_feature_importance(
        model=artifacts["model"],
        feature_names=artifacts["feature_names"],
        model_name=model_name,
        top_n=top_n
    )

    print("="*50)
    print(feature_importance)
    print(type(feature_importance))

    return {
        "dataset": dataset_name,
        "model": model_name,
        "feature_importance": feature_importance
    }