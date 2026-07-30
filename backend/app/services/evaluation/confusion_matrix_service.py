from sklearn.metrics import confusion_matrix
from app.services.persistence.model_loader import load_saved_model

def generate_confusion_matrix(
        model,
        X_test,
        y_test,
        class_names = None
):
    """
    Generate confusion matrix for classification models.
    """

    if not hasattr(model, "predict"):
        return None

    if not hasattr(model, "classes_"):
        return None

    y_pred = model.predict(X_test)

    matrix = confusion_matrix(
        y_test,
        y_pred
    )

    if class_names is None:
        class_names = sorted(list(set(y_test)))

    return {
        "labels": list(class_names),
        "matrix": matrix.tolist()
    }


def get_confusion_matrix(
        dataset_name,
        model_name
):

    artifacts = load_saved_model(
        dataset_name,
        model_name
    )

    return {

        "dataset": dataset_name,
        "model": model_name,
        "confusion_matrix": artifacts["confusion_matrix"]
    }