"""
Choose the right SHAP explainer for a given fitted model.

Rather than hardcoding a fixed list of imported classes (which breaks the
moment a new model type is added, or crashes if an optional library like
XGBoost isn't installed), model families are matched by class name. Any
model not recognized as linear or tree-based falls back to a
sample-limited KernelExplainer, which is model-agnostic but the slowest -
so the sample size is deliberately capped (settings.SHAP_MAX_ROWS_FOR_KERNEL_EXPLAINER)
to keep explainability computationally reasonable.
"""

import shap

from app.core.config import settings

LINEAR_MODEL_NAMES = {
    "LogisticRegression", "LinearRegression", "Ridge", "Lasso", "ElasticNet",
}

TREE_MODEL_NAMES = {
    "DecisionTreeClassifier", "DecisionTreeRegressor",
    "RandomForestClassifier", "RandomForestRegressor",
    "ExtraTreesClassifier", "ExtraTreesRegressor",
    "GradientBoostingClassifier", "GradientBoostingRegressor",
    "HistGradientBoostingClassifier", "HistGradientBoostingRegressor",
    "XGBClassifier", "XGBRegressor",
    "LGBMClassifier", "LGBMRegressor",
    "CatBoostClassifier", "CatBoostRegressor",
}


def get_shap_explainer(model, background_data):
    """
    Return the appropriate SHAP explainer based on the model type.
    """

    model_name = type(model).__name__

    if model_name in LINEAR_MODEL_NAMES:
        return shap.LinearExplainer(model, background_data)

    if model_name in TREE_MODEL_NAMES:
        return shap.TreeExplainer(model)

    # Model-agnostic fallback (KNN, SVM/SVR, Naive Bayes, AdaBoost, etc.)
    # Deliberately small background + prediction function to keep this
    # computationally reasonable - KernelExplainer is O(background_size).
    sample = background_data[: settings.SHAP_MAX_ROWS_FOR_KERNEL_EXPLAINER]

    predict_fn = model.predict_proba if hasattr(model, "predict_proba") else model.predict
    return shap.KernelExplainer(predict_fn, sample)
