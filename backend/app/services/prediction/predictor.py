from app.services.explainability.prediction_explainer import explain_prediction

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

    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation
    }