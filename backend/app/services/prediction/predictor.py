from app.services.explainability.prediction_explainer import explain_prediction
from app.services.explainability.probability import get_prediction_probabilities
from app.services.explainability.feature_importance import generate_feature_importance
from app.services.explainability.explanation_formatter import format_prediction_explanation

def predict(
        model,
        input_data,
        model_name,
        feature_names,
        label_encoder=None
):
    """
    Predict on a single sample using a trained model.
    """

    prediction = model.predict(input_data)[0]

    if hasattr(model, "predict_proba"):

        confidence = float(
                model.predict_proba(input_data).max()
            )

    else:

        confidence = None

    explanation = explain_prediction(
        model=model,
        model_name=model_name,
        prediction = prediction,
        input_data=input_data,
        feature_names=feature_names,
        label_encoder=label_encoder
    )

    probabilities = get_prediction_probabilities(
        model = model,
        input_data = input_data,
        label_encoder = label_encoder
    )

    feature_importance = generate_feature_importance(
        model = model,
        model_name = model_name,
        feature_names = feature_names
    )

    formatted_explanation = format_prediction_explanation(
        prediction = explanation.get("prediction"),
        confidence = explanation.get("confidence"),
        probabilities = probabilities,
        feature_importance = feature_importance,
        top_contributing_features = explanation.get("top_contributing_features")
    )

    return formatted_explanation