import logging

from app.services.prediction.predictor import predict
from app.services.explainability.prediction_explainer import explain_prediction
from app.services.explainability.shap_explainer import generate_shap_explanation

logger = logging.getLogger("mlforge.prediction")


def predict_single_sample(
        model,
        model_name,
        input_data,
        feature_names,
        background_data = None,
        label_encoder = None
):
    """
    Predict one sample and generate its explaination.
    """

    prediction_result = predict(
        model = model,
        input_data = input_data,
        model_name = model_name,
        feature_names=feature_names,
        label_encoder=label_encoder
    )

    explaination = explain_prediction(
        model = model,
        model_name = model_name,
        prediction = prediction_result["prediction"],
        input_data = input_data,
        feature_names = feature_names,
        label_encoder = label_encoder
    )

    if background_data is not None:

        try:

            shap_explanation = generate_shap_explanation(
                model = model,
                input_data = input_data,
                feature_names = feature_names,
                background_data = background_data
            )

        except Exception as e:

            logger.info("SHAP not supported for %s: %s", type(model).__name__, e)

            shap_explanation = None

    else:
        shap_explanation = []

    return {
        "prediction": prediction_result["prediction"],
        "confidence": prediction_result["confidence"],
        "explanation": explaination,
        "shap": shap_explanation
    }