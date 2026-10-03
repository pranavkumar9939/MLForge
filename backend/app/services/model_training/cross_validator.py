from sklearn.base import clone
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

CV_FOLDS = 5


def perform_cross_validation(model, X, y, preprocessor=None):
    """
    Performs k-fold cross validation.

    If `preprocessor` is given, X must be the RAW (untransformed) training
    features. Preprocessing is then re-fitted inside every fold, so the
    validation fold never influences imputation, scaling or encoding.
    """

    estimator = model
    if preprocessor is not None:
        estimator = Pipeline([
            ("prep", clone(preprocessor)),   # unfitted copy, refit per fold
            ("model", clone(model)),         # keeps the tuned hyperparameters
        ])

    scores = cross_val_score(
        estimator=estimator,
        X=X,
        y=y,
        cv=CV_FOLDS
    )

    return {
        "scores": scores.tolist(),
        "mean": float(scores.mean()),
        "std": float(scores.std())
    }