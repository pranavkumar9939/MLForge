import numpy as np


def _to_native(value):
    """Convert numpy scalar types to native Python types for JSON serialization."""
    if isinstance(value, np.generic):
        return value.item()
    return value


def explain_prediction(
        model,
        model_name,
        prediction,
        input_data,
        feature_names,
        label_encoder = None,
        top_n = 5
):

    prediction = np.asarray(model.predict(input_data)).reshape(-1)[0]

    if not hasattr(model, "classes_") or len(model.classes_) == 0:

        return {
            "prediction": float(prediction),
            "confidence": None,
            "top_contributing_features": []
        }
    
    prediction_index = list(model.classes_).index(prediction)

    display_prediction = prediction
    if label_encoder is not None:
        try:
            display_prediction = label_encoder.inverse_transform([prediction])[0]
        except Exception:
            display_prediction = prediction

    if hasattr(model, "predict_proba"):

        confidence = float(
            np.max(
                model.predict_proba(input_data)
            )
        )

    else:

        confidence = None

    if model_name == "Logistic Regression":

        coefficients = np.abs(model.coef_)

        # LogisticRegression.coef_ has shape (1, n_features) for binary
        # classification (a single decision boundary) and
        # (n_classes, n_features) for true multinomial multiclass. Only
        # index by class when there is actually one row per class.
        if coefficients.ndim > 1 and coefficients.shape[0] > 1:
            coefficients = coefficients[prediction_index]
        else:
            coefficients = coefficients.flatten()

        contributions = input_data[0]*coefficients

        feature_contribution = []

        for feature, value, contribution in zip(
            feature_names,
            input_data[0],
            contributions
        ):
            feature_contribution.append(
                {
                    "feature": feature,
                    "value": float(value),
                    "contribution": float(contribution)
                }
            )

        feature_contribution.sort(
            key=lambda x: abs(x["contribution"]),
            reverse=True
        )

        return {
            "prediction": _to_native(display_prediction),
            "confidence": confidence,
            "top_contributing_features": feature_contribution[:top_n]
        }

    else:

        return {
            "prediction": _to_native(display_prediction),
            "confidence": confidence,
            "top_contributing_features": []
        }