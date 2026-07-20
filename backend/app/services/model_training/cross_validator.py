from sklearn.model_selection import cross_val_score

CV_FOLDS = 5

def perform_cross_validation(model, X, y):
    """
    Performs k-fold cross validation.
    """

    scores = cross_val_score(
        estimator=model,
        X=X,
        y=y,
        cv=CV_FOLDS
    )

    return {
        "scores": scores.tolist(),
        "mean": float(scores.mean()),
        "std": float(scores.std())
    }

