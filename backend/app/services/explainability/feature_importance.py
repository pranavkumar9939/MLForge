import numpy as np

def generate_feature_importance(
        model,
        feature_names,
        model_name,
        top_n=10
):

    clean_names = []

    for feature in feature_names:


        clean_names.append(
            feature
            .replace("numerical__","")
            .replace("categorical__", "")
            .replace("_", "")
        )

    if hasattr(model, "feature_importances_"):

        importance = model.feature_importances_
    
    elif hasattr(model, "coef_"):

        coefficients = np.abs(model.coef_)

        if coefficients.ndim > 1:
            importance = coefficients.mean(axis=0)

        else:
            importance = coefficients

    else:
        # No usable importance source on this model (e.g. KNN, SVM, Naive
        # Bayes) - return an empty list rather than a differently-shaped
        # dict, so every caller can rely on a consistent list return type.
        return []

    feature_importance = [
        {
            "feature": feature,
            "importance": float(score)
        }
        for feature, score in zip(clean_names, importance)
    ]

    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    return feature_importance[:top_n]