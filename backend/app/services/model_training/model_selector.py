
MODEL_REGISTRY = {
    "Binary Classification": {

        "default_model_name": "Logistic Regression",

        "available_models": [
            {
                "name": "Logistic Regression",
                "type": "Linear Model"
            },
            {
                "name": "Decision Tree",
                "type": "Tree Based"
            },
            {
                "name": "Random Forest",
                "type": "Ensemble"
            }
        ],
        
        "reason": (
        "The target variable contains only two classes."
        "Logistic Regression is an excellent baseline because "
        "it is fast, interpretable, and performs well on binary classification problems."
        ),
        
        "limitations": [
         "cannot model complex nonlinear relationships"
        ]
    },

    "Regression": {

        "default_model_name": "Linear Regression",

        "available_models": [
            {
                "name": "Linear Regression",
                "type": "Linear Model"
            }
        ],
                
        "reason": (
            "Linear regression is chosen when predicting continuous numerical values (e.g., house prices) because it is simple, "
            "fast, and highly interpretable. "
            "It acts as an excellent baseline model due to its transparency and computational efficiency."
        ),
                
        "limitations": [
            "its main limitation is its inability to capture complex, non-linear relationships. "
            "It fails when data does not fit a straight-line pattern."
        ]
    },

    "Multi-Class Classification": {

        "default_model_name": "Decision Tree",

        "available_models": [
            {
                "name": "Logistic Regression",
                "type": "Linear Model"
            },
            {
                "name": "Decision Tree",
                "type": "Tree Based"
            },
            {
                "name": "Random Forest",
                "type": "Ensemble"
            }
        ],

        "reason": (
            "The target variable contains more than two classes. "
            "Decision Tree is selected as the default baseline because "
            "it can naturally handle multiclass classification, capture "
            "nonlinear decision boundaries, and requires minimal data preprocessing."
        ),

        "limitations": [
            "Cannot model highly complex nonlinear decision boundaries."
        ]
    }
}

def select_model(problem_type):
    """
    Select the best suitable ML model. 
    """

    if problem_type not in MODEL_REGISTRY:
        raise ValueError(
            f"Unsupported problem type: {problem_type}"
        )

    return MODEL_REGISTRY[problem_type]