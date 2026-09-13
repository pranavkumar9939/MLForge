"""
Hyperparameter search spaces for RandomizedSearchCV, keyed by model name.
Models without an entry here are trained with their default parameters
(no tuning attempted) - this is a deliberate choice for very fast/simple
baselines like Naive Bayes.
"""

PARAMETER_GRIDS = {

    # ---- Classification ----

    "Logistic Regression": {
        "C": [0.01, 0.1, 1, 10, 100],
    },

    "Decision Tree": {
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
    },

    "Random Forest": {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
    },

    "Extra Trees": {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20, 30],
    },

    "Gradient Boosting": {
        "n_estimators": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 4],
    },

    "HistGradientBoosting": {
        "max_iter": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [None, 5, 10],
    },

    "AdaBoost": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.5, 1.0],
    },

    "XGBoost": {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
    },

    "LightGBM": {
        "n_estimators": [100, 200, 300],
        "max_depth": [-1, 5, 10],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
    },

    "CatBoost": {
        "iterations": [100, 200, 300],
        "depth": [4, 6, 8],
        "learning_rate": [0.01, 0.05, 0.1],
    },

    "SVM": {
        "C": [0.1, 1, 10, 100],
        "gamma": ["scale", "auto"],
        "kernel": ["rbf", "linear"],
    },

    "KNN": {
        "n_neighbors": [3, 5, 7, 9],
        "weights": ["uniform", "distance"],
    },

    # ---- Regression ----

    "Ridge Regression": {
        "alpha": [0.01, 0.1, 1, 10, 100],
    },

    "Lasso Regression": {
        "alpha": [0.001, 0.01, 0.1, 1, 10],
    },

    "ElasticNet": {
        "alpha": [0.001, 0.01, 0.1, 1, 10],
        "l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9],
    },

    "Decision Tree Regressor": {
        "max_depth": [None, 5, 10, 20],
    },

    "Random Forest Regressor": {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
    },

    "Extra Trees Regressor": {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
    },

    "Gradient Boosting Regressor": {
        "n_estimators": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 4],
    },

    "HistGradientBoosting Regressor": {
        "max_iter": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
    },

    "XGBoost Regressor": {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
    },

    "LightGBM Regressor": {
        "n_estimators": [100, 200, 300],
        "max_depth": [-1, 5, 10],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
    },

    "CatBoost Regressor": {
        "iterations": [100, 200, 300],
        "depth": [4, 6, 8],
        "learning_rate": [0.01, 0.05, 0.1],
    },

    "SVR": {
        "C": [0.1, 1, 10],
        "kernel": ["rbf", "linear"],
    },

    "KNN Regressor": {
        "n_neighbors": [3, 5, 7, 9],
    },
}
