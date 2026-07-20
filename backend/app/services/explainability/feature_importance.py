import numpy as np

def generate_feature_importance(
        model,
        feature_names,
        model_name,
        top_n=10
):

    if hasattr(model, "feature_importances_"):

        importance = model.feature_importances_
    
    elif model_name == "Logistic Regression":

        coefficients = np.abs(model.coef_)

        if coefficients.ndim > 1:
            importance = coefficients.mean(axis=0)

        else:
            importance = coefficients

        feature_importance = [
            {
                "feature": feature,
                "importance": float(score)
            }
            for feature, score in zip(feature_names, importance)
        ]

        feature_importance.sort(
            key = lambda x: x["importance"],
            reverse = True
        )

        return feature_importance[:top_n]

    else:
        return []

    feature_importance = [
        {
            "feature": feature,
            "importance": float(score)
        }
        for feature, score in zip(feature_names, importance)
    ]

    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    return feature_importance[:top_n]