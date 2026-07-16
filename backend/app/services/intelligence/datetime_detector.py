import pandas as pd

def is_datetime_column(series, thresold=0.95):

    """
    Check whether a column is likely to contain datetime values.
    """

    # ignore missing values
    non_null = series.dropna()

    # empty column
    if len(non_null) == 0:
        return False

    # try convering values to datetime
    converted = pd.to_datetime(non_null, errors="coerce")

    # Count successfully converted values
    valid_dates = converted.notna().sum()

    # calculate success rate
    success_rate = valid_dates / len(non_null)

    return success_rate >= thresold