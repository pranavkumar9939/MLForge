def interpret_score(score, metric_name):
    """
    Interpret an evaluation metric score.
    """

    percentage = round(score * 100, 2)

    if score >= 0.90:
        status = "Excellent"
        color = "Green"

    elif score >= 0.80:
        status = "Good"
        color = "Light Green"

    elif score >= 0.70:
        status = "Fair"
        color = "Yellow"

    elif score >= 0.60:
        status = "Need Improvement"
        color = "Orange"

    else:
        status = "Poor"
        color = "Red"

    return {
        "metric": metric_name,
        "value": percentage,
        "status": status,
        "color": color,
        "explanation": generate_explanation(
            metric_name,
            percentage,
            status
        )
    }

def generate_explanation(metric_name, value, status):
    """
    Generate a human-readable explanation.
    """

    explanations = {
        "Accuracy":
        f"The model correctlty predicted {value}% of all samples."
        f"This is considered {status.lower()} performance.",

        "Precision":
        f"When the model predicts a positive class, it is correct {value}% of the time."
        f"This is considered {status.lower()} performance.",

        "Recall":
        f"The model successfully identified {value}% of the actual positive samples."
        f"This is considered {status.lower()} performance.",

        "F1 Score":
        f"The balance between Precision and Recall is {value}%"
        f"This is considered {status.lower()} performance."

    }

    return explanations.get(
        metric_name,
        "No Explanation available."
    )


def interpret_r2_score(score):
    """
    Interpret the R2 score of a regression model.
    """

    percentage = round(score * 100, 2)

    if score >= 0.90:
        status = "Excellent"
        color = "Green"
        explaination = "The model explains all variabilty in the target column."

    elif score >= 0.80:
        status = "Good"
        color = "Light Green"
        explaination = "The model explains almost most of the variability in the data."

    elif score >= 0.70:
        status = "Fair"
        color = "Yellow"
        explaination = "The model has acceptable predictive capability."

    elif score >= 0.60:
        status = "Needs Improvement"
        color = "Orange"
        explaination = "The model explains only one part of the variability."

    else:
        status = "Poor"
        color = "Red"
        explaination = "The model performs poorly and needs improvement."


    return {
        "status": status,
        "color": color,
        "explaination": explaination
    }