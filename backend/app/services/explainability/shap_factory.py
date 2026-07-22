import shap

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def get_shap_explainer(model, background_data):
    """
    Return the appropriate SHAP explainer based on the model type.
    """

    if isinstance(
        model,
        (
            LogisticRegression,
            LinearRegression
        )
    ):

        return shap.LinearExplainer(
            model,
            background_data
        )

    elif isinstance(
        model,
        (
            DecisionTreeRegressor,
            DecisionTreeClassifier,
            RandomForestRegressor,
            RandomForestClassifier
        )
    ):

        return shap.TreeExplainer(model)

    else:

        return shap.Explainer(
            model,
            background_data
        )


    