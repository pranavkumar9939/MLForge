def format_prediction_explanation(
        prediction,
        confidence,
        probabilities,
        feature_importance,
        top_contributing_features
):
    explanation = {
        "prediction": prediction,
        "confidence": confidence,
        "prediction_probabilities": probabilities,
        "feature_importance": feature_importance,
        "top_contributing_features": top_contributing_features
    }

    return explanation