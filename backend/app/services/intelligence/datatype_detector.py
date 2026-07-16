import pandas as pd

from app.services.intelligence.datetime_detector import is_datetime_column

def detect_column_type(series):
    """
    Detect the logical type of a pandas Series.
    """

    if pd.api.types.is_bool_dtype(series):
        return "Boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "Numerical"

    if is_datetime_column(series):
        return "Datetime"

    return "Categorical"

