from sklearn.linear_model import LogisticRegression

MODEL_REGISTRY = {
    "Binary Classification": {
        "name": "Logistic Regression",
        
        "model": LogisticRegression(),
        
        "type": "Linear Model",
        
        "reason": (
        "The target variable contains only two classes."
        "Logistic Regression is an excellent baseline because "
        "it is fast, interpretable, and performs well on binary classification problems."
        ),
        
        "Limitations": [
         "cannot model complex nonlinear relationships"
        ]
    }
}

def select_model(problem_type):
    """
    Select the best suitable ML model. 
    """

    return MODEL_REGISTRY.get(problem_type)