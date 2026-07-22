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

    print("=" * 50)
    print("values.shape:", values.shape)
    print("values.ndim:", values.ndim)
    print("type(values):", type(values))

    if hasattr(model, "classes_"):
        print("model.classes_:", model.classes_)

    print("prediction:", model.predict(input_data))
    print("=" * 50)

    # Binary classification / Regression
    if values.ndim == 2:
        values = values[0]

    # Multi-class classification
    elif values.ndim == 3:
        predicted_label = model.predict(input_data)[0]

        predicted_class_index = np.where(
            model.classes_ == predicted_label
        )[0][0]

        values = values[0, :, predicted_class_index]

    # elif values.ndim == 3:
    #     print(values)
    #     return []

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