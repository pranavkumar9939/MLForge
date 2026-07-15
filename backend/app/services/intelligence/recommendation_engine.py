def generate_recommendations(column_info):
    """
    Generate preprocessing recommendations for a column.
    """

    recommendations = []

    # identifying

    if column_info["is_identifier"]:
        recommendations.append({
            "action": "Removing Identifier Column",
            "reason": "Each value is unique, so this column does not provide useful information for model training.",
            "priority": "High"
        })
        return recommendations

    # missing values
    

    if column_info["missing"] > 0:

        if column_info["type"] == "Numerical":
            recommendations.append({
                "action": "Handle Missing values",
                "reason": "This numerical feature contains missing values. Filling them with the median preserves the distribution and is less sensitive to outliers than the mean.",
                "priority": "High"
            })

        else:
            recommendations.append({
                "action": "Handle Missing values",
                "reason": "This categorical feature contains missing values. Filling them with the mode preserves the most common category and is an appropriate strategy for categorical data.",
                "priority": "High"
            })

    # Datetime

    if column_info["type"] == "Datetime":
        recommendations.append({
            "action": "Extract Datetime feature",
            "reason": "Extract useful datetime features like year, month, and day.",
            "priority": "Low"
        })

    # Numerical 

    if column_info["type"] == "Numerical":
        recommendations.append({
            "action": "Scale feature",
            "reason": "Scaling numerical features improves the performance of many machine learning algorithms, especially those based on distance or gradient optimization.",
            "priority": "Medium"        
            })

    # Categorical

    if column_info["type"] == "Categorical":
        recommendations.append({
            "action": "Encode feature",
            "reason": "Machine learning algorithms require numerical input, so categorical values should be encoded before training.",
            "priority": "Low"
        })

    return recommendations