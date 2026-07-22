from sklearn.linear_model import LogisticRegression, LinearRegression

from app.services.explainability.shap_factory import get_shap_explainer
from app.services.explainability.explainers.linear_explainer import process_linear_shap

def generate_shap_explanation(
    model, 
    input_data,
    feature_names,
    background_data,
    top_n=10
):
    """
    Generate SHAP explanation using the correct explainer.
    """

    explainer = get_shap_explainer(
        model = model,
        background_data = background_data
    )

    if isinstance(
        model,
        (
            LogisticRegression,
            LinearRegression
        )
    ):

        return process_linear_shap(
            explainer = explainer,
            input_data = input_data,
            feature_names = feature_names,
            model = model,
            top_n = top_n
        )

    return {
        "supported": False,
        "message": "SHAP is not implemented for this model yet."
    }