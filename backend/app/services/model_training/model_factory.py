from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier



MODEL_FACTORY = {
    "Logistic Regression": lambda: LogisticRegression(max_iter=1000),

    "Linear Regression": lambda: LinearRegression(),

    "Decision Tree": lambda: DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": lambda: RandomForestClassifier(
         n_estimators=100,
         random_state=42
    )
}


def create_model(model_name):
    """
    Createa and return a ml model based on its name.
    """

    if model_name not in MODEL_FACTORY:
         raise ValueError(
             f"Unsupported model: {model_name}"
         )

    return MODEL_FACTORY[model_name]()