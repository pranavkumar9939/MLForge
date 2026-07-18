def generate_overall_assessment(results):
    """
    Generate an overall assessment of the trained model.
    """

    accuracy = results["accuracy"]
    precision = results["precision"]
    recall = results["recall"]
    f1 = results["f1_score"]

    average_score = (
        accuracy["value"] + 
        precision["value"] + 
        recall["value"] + 
        f1["value"]
    ) / 4

    if average_score >= 90:
        status = "Excellent"
        summary = "The model demonstrates excellent predictive performance across all evaluation metrics"
        recommendation = "The model is suitable for deployment after validation on unseen data."

    elif average_score >= 80:
        status = "Good"
        summary = "The model demonstrates good predictive performance across most evaluation metrics."
        recommendation = "Consider performing feature engineering to improve model performance."

    elif average_score >= 70:
        status = "Fair"
        summary = "The model demonstrates fair predictive performance but has room for improvement."
        recommendation = "Consider trying a different machine learning algorithm."

    elif average_score >= 60:
        status = "Needs Improvement"
        summary = "The current model has limited predictive performance"
        recommendation = "Consider improving data quality, feature engineering, or trying a different ML Algorithm."

    else:
        status = "Poor"
        summary = "The model demonstrates poor predictive performance and is not reliable for making predictions."
        recommendation = "Do some feature engineering along with data analysis and improve data quality and then retest it."

    return {
        "overall_score": round(average_score, 2),
        "status": status,
        "summary": summary,
        "recommendation": recommendation
    }

def generate_regression_assesment(results):
    """
    Generate an overall assessment for regression model.
    """

    r2_percentage = float(results["r2_score"])*100

    if r2_percentage >= 90:

        status = "Excellent"

        summary = "The regression model demonstrates excellent predictive performance."

        recommendation = "The model is suitable for deployment after validation on unseen data."

    elif r2_percentage >= 80:

        status = "Good"

        summary = "The model predicts the target variable with good accuracy."

        recommendation = "Consider feature enginering or comparing with ensemble regressors for further improvement."

    elif r2_percentage >= 70:

        status = "Fair"

        summary = "The model captures the overall trend but has room for improvement."

        recommendation = "Try additional features or alternative regression algorithms."

    elif r2_percentage >= 60:

        status = "Needs Improvement"

        summary = "The model has limited predictive capability."

        recommendation = "Improve data quality, engineer new features, or try more advanced regression models."

    else:

        status = "Poor"

        summary = "The model fails to explain much of the target variable."

        recommendation = "Investigate the dataset, perform feature enginnering, and consider a different modeling approach."

    return {
        "overall_score": round(r2_percentage, 2),

        "status": status,

        "summary": summary,

        "recommendation": recommendation
    }