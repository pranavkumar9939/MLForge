from sklearn.model_selection import RandomizedSearchCV

from app.core.config import settings
from .parameter_grids import PARAMETER_GRIDS


def tune_model(
        model,
        model_name,
        X_train,
        y_train,
        problem_type,
        training_mode: str = "balanced",
):
    """
    Hyperparameter-tune a model using RandomizedSearchCV, with the search
    budget (iterations, CV folds) controlled by `training_mode`:
    fast | balanced | thorough (see settings.TUNING_MODE_ITER/CV).

    If no parameter grid is defined for this model, it is simply fit as-is
    rather than failing - not every model needs or has a tuning grid.
    """

    if model_name not in PARAMETER_GRIDS:

        model.fit(X_train, y_train)

        return {
            "model": model,
            "best_params": {},
            "best_score": None,
            "tuned": False
        }

    n_iter = settings.TUNING_MODE_ITER.get(training_mode, settings.TUNING_MODE_ITER["balanced"])
    cv_folds = settings.TUNING_MODE_CV.get(training_mode, settings.TUNING_MODE_CV["balanced"])

    param_grid = PARAMETER_GRIDS[model_name]
    # RandomizedSearchCV requires n_iter <= number of possible combinations
    # for small discrete grids; cap it so it never errors out.
    max_combinations = 1
    for values in param_grid.values():
        max_combinations *= max(len(values), 1)
    n_iter = min(n_iter, max_combinations)

    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_grid,
        n_iter=n_iter,
        cv=cv_folds,
        scoring="r2" if problem_type == "Regression" else "accuracy",
        n_jobs=-1,
        random_state=42
    )

    search.fit(X_train, y_train)

    return {
        "model": search.best_estimator_,
        "best_params": search.best_params_,
        "best_score": search.best_score_,
        "tuned": True
    }
