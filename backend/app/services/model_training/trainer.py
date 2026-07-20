from sklearn.model_selection import train_test_split

from app.services.model_training.model_selector import select_model
from app.services.model_training.model_factory import create_model

from app.services.model_training.cross_validator import perform_cross_validation
from app.services.prediction.prediction_service import predict_single_sample

DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42

def train_model(X, 
    y, 
    analysis,
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

    for model_info_item in model_info["available_models"]:

        model_name = model_info_item["name"]

        model = create_model(model_name)

        model.fit(X_train, y_train)

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
            label_encoder = label_encoder 
        )
        
            
        

        trained_models.append({
            "model_name": model_name,
            "model_type": model_info_item["type"],
            "model": model,
            "predictions": predictions,
            "cross_validation": cv_result,
            "sample_prediction": sample_prediction
        })

    return {
        "problem_type": problem_type,

        "trained_models": trained_models,
        
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }