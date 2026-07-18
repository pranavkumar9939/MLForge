def generate_improvement_suggestions(results):
    """
    Generate intelligent insights and improvement suggestions based on the evaluation metrics.
    """

    suggestions = []

    accuracy = results["accuracy"]["value"]
    precision = results["precision"]["value"]
    recall = results["recall"]["value"]
    f1 = results["f1_score"]["value"]

    if accuracy >= 90:

        suggestions.append({

            "type": "Performance",
            "priority": "Low",

            "title": "Excellent Model Performance",

            "message": (
                "The model achieved excellent accuracy "
                "and is suitable for prediction after "
                "validation on unseen data."
            )
        })

    elif accuracy >= 80:

        suggestions.append({

            "type": "Performance",
            "priority": "Medium",

            "title": "Good Model Performance",

            "message": (
                "The model performs well and produces reliable predictions. "
                "Further improvements through feature engineering or "
                "hyperparameter tuning may increase performance."
            )
        })

    elif accuracy >= 70:

        suggestions.append({

            "type": "Performance",
            "priority": "High",

            "title": "Fair Model Performance",

            "message": (
                "The model demonstrates acceptable predictive performance "
                "but still has room for the improvement before deployment."
            )
    })

    else:

        suggestions.append({

            "type": "Performance",
            "priority": "High",

            "title": "Poor Model Performance",

            "message": (
                "The model performance is low and requires significant "
                "improvements before it can be considered reliable."
            )
        })


    if precision < recall:
        suggestions.append({

            "type": "Insight",

            "title": "Precision is lower than Recall",

            "message": (
                "The model predicts positive cases more "
                "aggressively, which may increase false positives."
            )
        })

    elif recall < precision:

        suggestions.append({

            "type": "Insight",

            "title": "Recall is lower than Precision",

            "message": (
                "The model is conservative while predicting "
                'positive cases may miss some actual positives.'
            )
        })

    else:

        suggestions.append({

            "type": "Insight",
            "priority": "Low",

            "title": "Balanced Precision and Recall",

            "message": (
                "The model maintains a healthy balance between precision "
                "and recall, indicating consistent prediction quality."
            )
        })

    if f1 < 70:

        suggestions.append({

            "type": "Warning",

            "title": "Balanced Performance Needed",

            "message": (
                "The F1-score indicates that precision "
                "and recall are not well balanced."
            )
        })

    if accuracy < 90:

        suggestions.append({

            "type": "Recommendation",
            "priority": "Medium",

            "title": "Try Another Algorithm",

            "message": (
                "Compare Logistic Regression with tree-based models such "
                "as Random Forest or Gradient Boosting to determine whether "
                "better predictive performance can be achieved."
            )
        })

    else:

        suggestions.append({

            "type": "Recommendation",
            "priority": "Low",

            "title": "Validate Before Deployment",

            "message": (
                "The current model performs very well. Validate it using "
                "cross-validation or an independent test dataset before "
                "deploying it in production."
            )
        })

    return suggestions




def generate_regression_improvement_suggestions(results):
    """
    Generate intelligent suggestions for regression models.
    """

    suggestions = []

    r2 = results["r2_score"]
    mae = results["mae"]
    rmse = results["rmse"]

    # Excellent model
    if r2 >= 0.90:

        suggestions.append({
            "type": "Performance",
            "title": "Excellent Regression Model",
            "message": (
                "The model explains most of the variance in the target variable "
                "and is suitable for prediction after validation on unseen data."
            )
        })

    # Good model
    elif r2 >= 0.80:

        suggestions.append({
            "type": "Performance",
            "title": "Good Model Performance",
            "message": {
                "The model predicts the target variaable well, "
                "although further optimization improve accuracy."
            }
        })

    # Fair model
    elif r2 >= 0.70:

        suggestions.append({
            "type": "Warning",
            "title": "Moderate Predictive Power",
            "message": (
                "The model covers the general trend nut still leaves "
                "significant unexplained variation."
            )
        })

    # needs imprvement
    else:

        suggestions.append({
            "type": "Warning",
            "title": "Model Needs Improvement",
            "message": (
                "The regression model has limited predictive capability. "
                "Feature engineering or a different algoruthm is recommended."
            )
        })

    # High prediction error
    if rmse > mae * 1.5:

        suggestions.append({
            "type": "Insight",
            "title": "Large Predicton Errors Detected",
            "message": (
                "RMSE is significantly higher than MAE, suggesting that "
                "some predictions contain large error (otliers)."
            )
        })

    # General recommendation

    suggestions.append({
        "type": "Recommendation",
        "title": "Compare Multiple Algorithms",
        "message": (
            "Compare Linear Regression with random Forest Regressor, "
            "Gradient Boosting, XGBoost, or CatBoost to determine whether "
            "a better-performing model exists."
        )
    })

    return suggestions