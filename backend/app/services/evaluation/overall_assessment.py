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
        "overall_score": average_score,
        "status": status,
        "summary": summary,
        "recommendation": recommendation
    }