import numpy as np

def process_linear_shap(
        explainer,
        input_data,
        feature_names,
        model,
        top_n = 10
):
    """
    Process SHAP values for linear models.
    """

    shap_values = explainer(input_data)
    values = shap_values.values

    # Binary classification / Regression
    if values.ndim == 2:
        values = values[0]

    # Multi-class classification
    elif values.ndim == 3:
        predicted_label = np.asarray(model.predict(input_data)).reshape(-1)[0]
        predicted_class_index = np.where(
            model.classes_ == predicted_label
        )[0][0]

        values = values[0, :, predicted_class_index]

    feature_contributions = []

    for feature, value in zip(feature_names, values):

        feature_contributions.append(
            {
                "feature": feature,
                "shap_value": float(value),
                "impact": abs(float(value))
            }
        )

    feature_contributions.sort(
        key = lambda x: x["impact"],
        reverse = True
    )

    return feature_contributions[:top_n]