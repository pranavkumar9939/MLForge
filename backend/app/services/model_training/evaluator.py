from sklearn.metrics import (
    accuracy_score, 
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def evaluate_model(training_result):
    """
    Evaluate the trained machine learning model.
    """

    y_test = training_result["y_test"]
    predictions = training_result["predictions"]
    model_name = training_result["model_name"]
    problem_type = training_result["problem_type"]

    if problem_type == "Binary Classification":

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        cm = confusion_matrix(
            y_test,
            predictions
        )

        report = classification_report(
            y_test,
            predictions,
            output_dict=True
        )

        return {

            "model_name": model_name,

            "problem_type": problem_type,

            "accuracy": round(accuracy,4),

            "precision": round(precision,4),

            "recall": round(recall,4),

            "f1_score": round(f1,4),

            "confusion_matrix": cm.tolist(),

            "classification_report": report,

            "summary": {
                "total_predictions": len(predictions),
                "correct_predictions": int((predictions == y_test).sum())
            }
        }

    raise ValueError(
        f"Evaluation for'{problem_type}' is not implemented."
    )

    