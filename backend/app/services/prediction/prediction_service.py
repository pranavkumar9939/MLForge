from app.services.prediction.predictor import predict
from app.services.explainability.prediction_explainer import explain_prediction

def predict_single_sample(
        model,
        model_name,
        input_data,
        feature_names,
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

    return {
        "prediction": prediction_result["prediction"],
        "confidence": prediction_result["confidence"],
        "explanation": explaination
    }