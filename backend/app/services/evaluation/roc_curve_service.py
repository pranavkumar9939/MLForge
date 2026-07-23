import numpy as np

from sklearn.metrics import roc_curve, auc

from sklearn.preprocessing import label_binarize

def generate_roc_curve(
        model,
        X_test,
        y_test,
        problem_type,
        class_names = None
):
    """
    Generate ROC Curve data for Binary and Multi-Class Classification.
    """

    if "Regression" in problem_type:
        return None

    if not hasattr(model, "predict_proba"):
        return None

    probabilities = model.predict_proba(X_test)

    # binary classification

    if probabilities.shape[1] == 2:

        fpr, tpr, _ = roc_curve(
            y_test,
            probabilities[:, 1]
        )

        roc_auc = auc(fpr, tpr)

        return {
            "type": "binary",
            "auc": float(roc_auc),
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist()
        }


    # multi class classification

    y_test_bin = label_binarize(
        y_test,
        classes = model.classes_
    )

    curves = []
    

    for i in range(probabilities.shape[1]):

        fpr, tpr, _ = roc_curve(
            y_test_bin[:,i],
            probabilities[:, i]
        )

        roc_auc = auc(fpr, tpr)

        if class_names is not None:
            class_label = str(class_names[i])

        else:
            class_label = str(model.classes_[i])

        curves.append({
            "class": class_label,
            "auc": float(roc_auc),
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist()
        })

    return {
        "type": "multiclass",
        "curves": curves
    }