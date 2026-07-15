import pandas as pd

def detect_column_type(series):
    """
    Detect the logical type of a pandas Series.
    """

    if pd.api.types.is_bool_dtype(series):
        return "Boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "Numerical"

    # Converting object column to datetime

    if series.dtype == "object":
        try:
            pd.to_datetime(series.dropna(), errors="raise")
            return "Datetime"

        except Exception:
            pass

    if pd.api.types.is_datetime64_any_dtype(series):
        return "Datetime"

    return "Categorical"

