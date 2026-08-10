import numpy as np
from sklearn.model_selection import train_test_split

from app.services.model_training.model_selector import select_model
from app.services.model_training.model_factory import create_model

from app.services.model_training.cross_validator import perform_cross_validation
from app.services.prediction.prediction_service import predict_single_sample
from app.services.evaluation.roc_curve_service import generate_roc_curve
from app.services.evaluation.confusion_matrix_service import generate_confusion_matrix

from app.services.hyperparameter.tuner import tune_model


DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42


def train_model(
    X, 
    y, 
    analysis,
    pipeline = None,
    feature_names = None,
    label_encoder = None
    ):
    """
    Automatically train the selected machine learning model.
    """

    problem_type = analysis["problem_type"]

    model_info = select_model(problem_type)
    if model_info is None:
        raise ValueError(
            f"No model available for '{problem_type}'"
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= DEFAULT_TEST_SIZE,
        random_state=DEFAULT_RANDOM_STATE
    )

    trained_models = []

    sample_size = min(100, len(X_train))

    indices = np.random.choice(
        len(X_train),
        sample_size,
        replace=False
    )

    for model_info_item in model_info["available_models"]:

        model_name = model_info_item["name"]

        print(
            "MODEL SELECTED:",
            model_name,
            "| Problem:",
            problem_type
        )

        model = create_model(model_name, problem_type)

        print(
            "MODEL CREATED:",
            type(model).__name__
        )

        # model.fit(X_train, y_train)

        tuning_result = tune_model(
            model = model,
            model_name = model_name,
            X_train = X_train,
            y_train = y_train,
            problem_type = problem_type
        )

        model = tuning_result["model"]

        cv_result = perform_cross_validation(
            model,
            X,
            y
        )

        predictions = model.predict(X_test)

        sample_prediction = predict_single_sample(
            model = model,
            model_name = model_name,
            input_data = X_test[[0]],
            feature_names = feature_names,
            background_data = X_train[indices],
            label_encoder = label_encoder 
        )

        print(label_encoder)
        print(type(label_encoder))

        roc_curve = None
        confusion_matrix = None

        if problem_type != "Regression":
        
            roc_curve = generate_roc_curve(
                model = model,
                X_test = X_test,
                y_test = y_test,
                problem_type = problem_type,
                class_names = label_encoder.classes_ if label_encoder else None
            )

            confusion_matrix = generate_confusion_matrix(
                model = model,
                X_test = X_test,
                y_test = y_test,
                class_names = (
                    label_encoder.classes_.tolist()
                    if label_encoder is not None
                    else None
                )
            )

        print("\n========== CONFUSION MATRIX ==========")
        print(confusion_matrix)
        print("======================================\n")
        

        trained_models.append({
            "model_name": model_name,
            "model_type": model_info_item["type"],
            "model": model,
            "predictions": predictions,
            "cross_validation": cv_result,
            "sample_prediction": sample_prediction,
            "roc_curve": roc_curve,
            "confusion_matrix": confusion_matrix,
            "tuned": tuning_result["tuned"],
            "best_params": tuning_result.get("best_params", {}),
            "best_cv_score": tuning_result.get("best_score", None),
        })


    return {
        "problem_type": problem_type,

        "trained_models": trained_models,
        
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,

        "pipeline": pipeline,
        "feature_names": feature_names,
        "label_encoder": label_encoder,
        "analysis": analysis,
        "roc_curve": roc_curve,
        "confusion_matrix": confusion_matrix
    }