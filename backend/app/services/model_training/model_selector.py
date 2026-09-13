"""
Problem-type -> candidate-algorithm mapping.

`select_model` filters the full candidate list down to models that are
actually available in this environment (see model_factory's optional
dependency handling), so an uninstalled library never surfaces in the UI
or crashes training.
"""

from app.services.model_training.model_factory import is_model_available

_FULL_MODEL_REGISTRY = {

    "Binary Classification": {

        "default_model_name": "Logistic Regression",

        "available_models": [
            {"name": "Logistic Regression", "type": "Linear Model"},
            {"name": "Decision Tree", "type": "Tree Based"},
            {"name": "Random Forest", "type": "Ensemble"},
            {"name": "Extra Trees", "type": "Ensemble"},
            {"name": "Gradient Boosting", "type": "Ensemble (Boosting)"},
            {"name": "HistGradientBoosting", "type": "Ensemble (Boosting)"},
            {"name": "AdaBoost", "type": "Ensemble (Boosting)"},
            {"name": "XGBoost", "type": "Ensemble (Boosting)"},
            {"name": "LightGBM", "type": "Ensemble (Boosting)"},
            {"name": "CatBoost", "type": "Ensemble (Boosting)"},
            {"name": "Naive Bayes", "type": "Probabilistic"},
            {"name": "KNN", "type": "Distance Based"},
            {"name": "SVM", "type": "Kernel Based"},
        ],

        "reason": (
            "The target variable contains only two classes. "
            "Logistic Regression is used as an interpretable baseline, "
            "and a broad mix of tree-based, boosting, and kernel models "
            "is trained alongside it so the strongest performer for this "
            "specific dataset can be identified."
        ),

        "limitations": [
            "Individual model limitations vary; see each model's card in the leaderboard."
        ]
    },

    "Multi-Class Classification": {

        "default_model_name": "Random Forest",

        "available_models": [
            {"name": "Logistic Regression", "type": "Linear Model"},
            {"name": "Decision Tree", "type": "Tree Based"},
            {"name": "Random Forest", "type": "Ensemble"},
            {"name": "Extra Trees", "type": "Ensemble"},
            {"name": "Gradient Boosting", "type": "Ensemble (Boosting)"},
            {"name": "HistGradientBoosting", "type": "Ensemble (Boosting)"},
            {"name": "AdaBoost", "type": "Ensemble (Boosting)"},
            {"name": "XGBoost", "type": "Ensemble (Boosting)"},
            {"name": "LightGBM", "type": "Ensemble (Boosting)"},
            {"name": "CatBoost", "type": "Ensemble (Boosting)"},
            {"name": "Naive Bayes", "type": "Probabilistic"},
            {"name": "KNN", "type": "Distance Based"},
            {"name": "SVM", "type": "Kernel Based"},
        ],

        "reason": (
            "The target variable contains more than two classes. "
            "Tree-based and ensemble models naturally handle multiclass "
            "problems and nonlinear decision boundaries with minimal "
            "preprocessing, so a broad mix is trained for comparison."
        ),

        "limitations": [
            "Individual model limitations vary; see each model's card in the leaderboard."
        ]
    },

    "Regression": {

        "default_model_name": "Random Forest Regressor",

        "available_models": [
            {"name": "Linear Regression", "type": "Linear Model"},
            {"name": "Ridge Regression", "type": "Linear Model (Regularized)"},
            {"name": "Lasso Regression", "type": "Linear Model (Regularized)"},
            {"name": "ElasticNet", "type": "Linear Model (Regularized)"},
            {"name": "Decision Tree Regressor", "type": "Tree Based"},
            {"name": "Random Forest Regressor", "type": "Ensemble"},
            {"name": "Extra Trees Regressor", "type": "Ensemble"},
            {"name": "Gradient Boosting Regressor", "type": "Ensemble (Boosting)"},
            {"name": "HistGradientBoosting Regressor", "type": "Ensemble (Boosting)"},
            {"name": "XGBoost Regressor", "type": "Ensemble (Boosting)"},
            {"name": "LightGBM Regressor", "type": "Ensemble (Boosting)"},
            {"name": "CatBoost Regressor", "type": "Ensemble (Boosting)"},
            {"name": "KNN Regressor", "type": "Distance Based"},
            {"name": "SVR", "type": "Kernel Based"},
        ],

        "reason": (
            "The target variable is continuous. Linear models act as an "
            "interpretable baseline, while tree-based and boosting models "
            "are trained alongside them to capture nonlinear relationships."
        ),

        "limitations": [
            "Individual model limitations vary; see each model's card in the leaderboard."
        ]
    },
}


def select_model(problem_type):
    """
    Return the candidate-model configuration for a problem type, filtered
    to only the models that are actually available in this environment.
    """

    if problem_type not in _FULL_MODEL_REGISTRY:
        raise ValueError(
            f"Unsupported problem type: {problem_type}"
        )

    config = dict(_FULL_MODEL_REGISTRY[problem_type])

    config["available_models"] = [
        m for m in config["available_models"] if is_model_available(m["name"])
    ]

    return config
