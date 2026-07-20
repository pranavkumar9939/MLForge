import numpy as np

def explain_prediction(
        model,
        model_name,
        prediction,
        input_data,
        feature_names,
        label_encoder = None,
        top_n = 5
):

    prediction = model.predict(input_data)[0]
    prediction_index = list(model.classes_).index(prediction)

    # if label_encoder is not None:

    #     prediction = label_encoder.inverse_transform([prediction_index])[0]

    if hasattr(model, "predict_proba"):

        confidence = float(
            np.max(
                model.predict_proba(input_data)
            )
        )

    else:

        confidence = None

    if model_name == "Logistic Regression":

        print(prediction_index)
        print(type(prediction_index))
        # print(coefficients.shape)
        print(label_encoder)
        coefficients = np.abs(model.coef_)

        # Multi Class
        if coefficients.ndim > 1:
            coefficients = coefficients[prediction_index]

        # binary classification

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
            "prediction": prediction,
            "confidence": confidence,
            "top_contributing_features": feature_contribution[:top_n]
        }

    else:

        return {
            "prediction": prediction,
            "confidence": confidence,
            "top_contributing_features": []
        }