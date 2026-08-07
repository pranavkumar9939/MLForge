from app.services.persistence.model_loader import load_saved_model


def get_metrics(
        dataset_name,
        model_name
):

    artifacts = load_saved_model(
        dataset_name,
        model_name
    )

    evaluation = artifacts["evaluation"]

    problem_type = evaluation.get(
        "problem_type",
        ""
    )

    # Regression
    if problem_type == "Regression":

        return {
            "dataset": dataset_name,
            "model": model_name,
            "problem_type": "Regression",

            "r2_score": evaluation.get(
                "r2_score",
                0
            ),

            "mae": evaluation.get(
                "mae",
                0
            ),

            "rmse": evaluation.get(
                "rmse",
                0
            ),

            "status": evaluation.get(
                "overall_assessment",
                {}
            ).get(
                "status",
                "Unknown"
            )
        }

    # Classification
    return {
        "dataset": dataset_name,
        "model": model_name,
        "problem_type": problem_type,

        "accuracy": evaluation.get(
            "accuracy",
            {}
        ).get(
            "value",
            0
        ),

        "precision": evaluation.get(
            "precision",
            {}
        ).get(
            "value",
            0
        ),

        "recall": evaluation.get(
            "recall",
            {}
        ).get(
            "value",
            0
        ),

        "f1_score": evaluation.get(
            "f1_score",
            {}
        ).get(
            "value",
            0
        )
    }