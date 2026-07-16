from sklearn.model_selection import train_test_split

from app.services.model_training.model_selector import select_model

DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42

def train_model(X, y, analysis):
    """
    Automatically train the selected machine learning model.
    """

    problem_type = analysis["problem_type"]

    model_info = select_model(problem_type)
    if model_info is None:
        raise ValueError(
            f"No model available for '{problem_type}'"
        )
    model = model_info["model"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= DEFAULT_TEST_SIZE,
        random_state=DEFAULT_RANDOM_STATE
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return {
        "model": model,
        "model_name": model_info["name"],
        "problem_type": problem_type,
        "predictions": predictions,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }