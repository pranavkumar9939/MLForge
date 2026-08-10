from sklearn.model_selection import RandomizedSearchCV

from .parameter_grids import PARAMETER_GRIDS

def tune_model(
        model,
        model_name,

        X_train,
        y_train,
        problem_type
):

    if model_name not in PARAMETER_GRIDS:

        model.fit(X_train, y_train)

        return {
            "model": model,
            "best_params": {},
            "best_score": None,
            "tuned": False
        }

    search = RandomizedSearchCV(
        estimator = model,

        param_distributions = PARAMETER_GRIDS[model_name],

        n_iter = 10,

        cv = 3,

        scoring = "r2" if problem_type == "Regression" else "accuracy",

        n_jobs = -1,

        random_state = 42

    )

    search.fit(X_train, y_train)

    return {
        "model": search.best_estimator_,

        "best_params": search.best_params_,

        "best_score": search.best_score_,

        "tuned": True
    }