from sklearn.linear_model import LogisticRegression, LinearRegression


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
    },

    "Regression": {
        "name": "Linear Regression",
                
        "model": LinearRegression(),
                
        "type": "Linear Model",
                
        "reason": (
            "Linear regression is chosen when predicting continuous numerical values (e.g., house prices) because it is simple, "
            "fast, and highly interpretable. "
            "It acts as an excellent baseline model due to its transparency and computational efficiency."
        ),
                
        "Limitations": [
            " its main limitation is its inability to capture complex, non-linear relationships. "
            "It fails when data does not fit a straight-line pattern."
        ]
    }
}

def select_model(problem_type):
    """
    Select the best suitable ML model. 
    """

    return MODEL_REGISTRY.get(problem_type)