import logging

import numpy as np
from sklearn.model_selection import train_test_split

from app.core.config import settings
from app.services.model_training.model_selector import select_model
from app.services.model_training.model_factory import create_model, EXPENSIVE_MODELS

from app.services.model_training.cross_validator import perform_cross_validation
from app.services.prediction.prediction_service import predict_single_sample
from app.services.evaluation.roc_curve_service import generate_roc_curve
from app.services.evaluation.confusion_matrix_service import generate_confusion_matrix

from app.services.hyperparameter.tuner import tune_model


logger = logging.getLogger("mlforge.trainer")

DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42


def train_model(
    X,
    y,
    analysis,
    pipeline=None,
    feature_names=None,
    label_encoder=None,
    training_mode="balanced",
    on_progress=None,
):
    """
    Automatically train every candidate model for the detected problem type.

    `on_progress(stage: str, current: int, total: int)` is called before
    each model starts training so callers (e.g. an async job) can surface
    real, backend-driven progress instead of a decorative spinner.
    """

    def report(stage, current, total):
        if on_progress:
            on_progress(stage, current, total)

    problem_type = analysis["problem_type"]

    model_info = select_model(problem_type)
    if model_info is None:
        raise ValueError(
            f"No model available for '{problem_type}'"
        )

    # Use stratified splitting for classification so class proportions are
    # preserved in both the train and test sets.
    is_classification = "Classification" in problem_type
    stratify = y if is_classification else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=DEFAULT_TEST_SIZE,
        random_state=DEFAULT_RANDOM_STATE,
        stratify=stratify
    )

    n_train_rows = len(X_train)

    # Intelligent model selection: skip computationally expensive models
    # (SVM, KNN and other O(n^2)-ish estimators) once the dataset is large
    # enough that training all of them would be impractical, rather than
    # blindly training every candidate regardless of dataset size.
    candidate_models = model_info["available_models"]
    skipped_models = []

    if n_train_rows > settings.MAX_ROWS_FOR_EXPENSIVE_MODELS:
        filtered = []
        for item in candidate_models:
            if item["name"] in EXPENSIVE_MODELS:
                skipped_models.append(item["name"])
            else:
                filtered.append(item)
        candidate_models = filtered or candidate_models  # never end up with zero candidates

    total_models = len(candidate_models)

    trained_models = []

    sample_size = min(settings.SHAP_BACKGROUND_SAMPLE_SIZE, n_train_rows)

    indices = np.random.default_rng(seed=DEFAULT_RANDOM_STATE).choice(
        n_train_rows,
        sample_size,
        replace=False
    )

    for position, model_info_item in enumerate(candidate_models, start=1):

        model_name = model_info_item["name"]

        report(f"Training {model_name} ({position}/{total_models})", position - 1, total_models)

        model = create_model(model_name, problem_type)

        tuning_result = tune_model(
            model=model,
            model_name=model_name,
            X_train=X_train,
            y_train=y_train,
            problem_type=problem_type,
            training_mode=training_mode,
        )

        model = tuning_result["model"]

        report(f"Cross-validating {model_name}", position - 1, total_models)

        # Cross-validate on the TRAINING split only. Using the full X, y
        # here would leak information from the held-out test set into the
        # reported CV score.
        cv_result = perform_cross_validation(
            model,
            X_train,
            y_train
        )

        predictions = model.predict(X_test)
        predictions = np.asarray(predictions).reshape(-1)
        

        sample_prediction = predict_single_sample(
            model=model,
            model_name=model_name,
            input_data=X_test[[0]],
            feature_names=feature_names,
            background_data=X_train[indices],
            label_encoder=label_encoder
        )

        roc_curve = None
        confusion_matrix = None

        if problem_type != "Regression":

            roc_curve = generate_roc_curve(
                model=model,
                X_test=X_test,
                y_test=y_test,
                problem_type=problem_type,
                class_names=label_encoder.classes_ if label_encoder is not None else None
            )

            confusion_matrix = generate_confusion_matrix(
                model=model,
                X_test=X_test,
                y_test=y_test,
                class_names=(
                    label_encoder.classes_.tolist()
                    if label_encoder is not None
                    else None
                )
            )

        logger.info("Trained %s | confusion_matrix=%s", model_name, confusion_matrix)

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

        report(f"Finished {model_name} ({position}/{total_models})", position, total_models)

    return {
        "problem_type": problem_type,

        "trained_models": trained_models,
        "skipped_models": skipped_models,

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
