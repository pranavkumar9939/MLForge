from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR



MODEL_FACTORY = {

     # Classification
     
    "Logistic Regression": lambda: LogisticRegression(max_iter=1000),

    "Decision Tree": lambda: DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": lambda: RandomForestClassifier(
         n_estimators=100,
         random_state=42
    ),

    "KNN": lambda: KNeighborsClassifier(
         n_neighbors=5
    ),

    "SVM": lambda: SVC(
         probability=True,
         random_state=42
    ),

    # Regression

    "Linear Regression": lambda: LinearRegression(),

    "Decision Tree Regressor": lambda: DecisionTreeRegressor(
         random_state=42
    ),

    "Random Forest Regressor": lambda: RandomForestRegressor(
         n_estimators=100,
         random_state=42
    ),

    "KNN Regressor": lambda: KNeighborsRegressor(
         n_neighbors=5
    ),

    "SVR": lambda: SVR()
}


def create_model(model_name, problem_type):
    """
    Createa and return a ml model based on its name.
    """

    if model_name not in MODEL_FACTORY:
         raise ValueError(
             f"Unsupported model: {model_name}"
         )

    return MODEL_FACTORY[model_name]()