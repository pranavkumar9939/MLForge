"""
Model factory: creates a fresh, unfitted estimator instance by name.

Gradient-boosting libraries (XGBoost, LightGBM, CatBoost) are optional
dependencies. If they are not installed, they are simply excluded from
MODEL_FACTORY (and therefore from model_selector's available_models lists)
instead of crashing the application - MLForge degrades gracefully rather
than requiring every optional ML library to be present.
"""

import logging

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
    Ridge,
    Lasso,
    ElasticNet,
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    AdaBoostClassifier,
)
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.naive_bayes import GaussianNB

logger = logging.getLogger("mlforge.model_factory")

# Models that are computationally expensive at scale (kernel/distance based)
# and get excluded first once a dataset is large.
EXPENSIVE_MODELS = {"SVM", "SVR", "KNN", "KNN Regressor"}


MODEL_FACTORY = {

    # ---- Classification ----

    "Logistic Regression": lambda: LogisticRegression(max_iter=1000),

    "Decision Tree": lambda: DecisionTreeClassifier(random_state=42),

    "Random Forest": lambda: RandomForestClassifier(n_estimators=100, random_state=42),

    "Extra Trees": lambda: ExtraTreesClassifier(n_estimators=100, random_state=42),

    "Gradient Boosting": lambda: GradientBoostingClassifier(random_state=42),

    "HistGradientBoosting": lambda: HistGradientBoostingClassifier(random_state=42),

    "AdaBoost": lambda: AdaBoostClassifier(random_state=42),

    "Naive Bayes": lambda: GaussianNB(),

    "KNN": lambda: KNeighborsClassifier(n_neighbors=5),

    "SVM": lambda: SVC(probability=True, random_state=42),

    # ---- Regression ----

    "Linear Regression": lambda: LinearRegression(),

    "Ridge Regression": lambda: Ridge(random_state=42),

    "Lasso Regression": lambda: Lasso(random_state=42),

    "ElasticNet": lambda: ElasticNet(random_state=42),

    "Decision Tree Regressor": lambda: DecisionTreeRegressor(random_state=42),

    "Random Forest Regressor": lambda: RandomForestRegressor(n_estimators=100, random_state=42),

    "Extra Trees Regressor": lambda: ExtraTreesRegressor(n_estimators=100, random_state=42),

    "Gradient Boosting Regressor": lambda: GradientBoostingRegressor(random_state=42),

    "HistGradientBoosting Regressor": lambda: HistGradientBoostingRegressor(random_state=42),

    "KNN Regressor": lambda: KNeighborsRegressor(n_neighbors=5),

    "SVR": lambda: SVR(),
}


# ---- Optional heavy dependencies: included only if installed ----

try:
    from xgboost import XGBClassifier, XGBRegressor

    MODEL_FACTORY["XGBoost"] = lambda: XGBClassifier(
        eval_metric="logloss", random_state=42
    )
    MODEL_FACTORY["XGBoost Regressor"] = lambda: XGBRegressor(random_state=42)
except ImportError:
    logger.info("xgboost is not installed - XGBoost models will be unavailable.")

try:
    from lightgbm import LGBMClassifier, LGBMRegressor

    MODEL_FACTORY["LightGBM"] = lambda: LGBMClassifier(random_state=42, verbosity=-1)
    MODEL_FACTORY["LightGBM Regressor"] = lambda: LGBMRegressor(random_state=42, verbosity=-1)
except ImportError:
    logger.info("lightgbm is not installed - LightGBM models will be unavailable.")

try:
    from catboost import CatBoostClassifier, CatBoostRegressor

    MODEL_FACTORY["CatBoost"] = lambda: CatBoostClassifier(random_state=42, verbose=False, allow_writing_files=False)
    MODEL_FACTORY["CatBoost Regressor"] = lambda: CatBoostRegressor(random_state=42, verbose=False, allow_writing_files=False)
except ImportError:
    logger.info("catboost is not installed - CatBoost models will be unavailable.")


def create_model(model_name, problem_type):
    """
    Create and return an ML model instance based on its name.
    """

    if model_name not in MODEL_FACTORY:
        raise ValueError(
            f"Unsupported or unavailable model: {model_name}"
        )

    return MODEL_FACTORY[model_name]()


def is_model_available(model_name: str) -> bool:
    return model_name in MODEL_FACTORY
