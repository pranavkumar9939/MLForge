from sklearn.base import clone
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from app.core.config import settings
from .parameter_grids import PARAMETER_GRIDS


def tune_model(
        model,
        model_name,
        X_train,            # RAW training features (untransformed)
        y_train,
        problem_type,
        preprocessor,       # UNFITTED ColumnTransformer
        training_mode: str = "balanced",
):
    """
    Tunes inside a Pipeline so preprocessing is re-fitted in every CV fold.
    Returns the fitted *model step only*, trained on features produced by
    the preprocessor fitted on the full training split, so the rest of the
    trainer (predict on transformed X_test, SHAP, ROC, saving) is unchanged.
    """

    pipe = Pipeline([
        ("prep", clone(preprocessor)),
        ("model", model),
    ])

    if model_name not in PARAMETER_GRIDS:
        pipe.fit(X_train, y_train)
        return {
            "model": pipe.named_steps["model"],
            "best_params": {},
            "best_score": None,
            "tuned": False
        }

    n_iter = settings.TUNING_MODE_ITER.get(training_mode, settings.TUNING_MODE_ITER["balanced"])
    cv_folds = settings.TUNING_MODE_CV.get(training_mode, settings.TUNING_MODE_CV["balanced"])

    param_grid = {f"model__{k}": v for k, v in PARAMETER_GRIDS[model_name].items()}

    max_combinations = 1
    for values in param_grid.values():
        max_combinations *= max(len(values), 1)
    n_iter = min(n_iter, max_combinations)

    search = RandomizedSearchCV(
        estimator=pipe,
        param_distributions=param_grid,
        n_iter=n_iter,
        cv=cv_folds,
        scoring="r2" if problem_type == "Regression" else "accuracy",
        n_jobs=-1,
        random_state=42
    )

    search.fit(X_train, y_train)

    best_params = {k.replace("model__", "", 1): v for k, v in search.best_params_.items()}

    return {
        "model": search.best_estimator_.named_steps["model"],
        "best_params": best_params,      # same format as before, for the UI
        "best_score": search.best_score_,
        "tuned": True
    }