import pandas as pd

def get_column_groups(df: pd.DataFrame):
    """
    Seperate dataset columns into numerical, categorical groups, and datetime.
    """

    numerical_columns = (
        df.select_dtypes(include=["number"]).columns.tolist()
    )

    categorical_columns = (
        df.select_dtypes(include=["object","category"]).columns.tolist()
    )

    datetime_columns = (
        df.select_dtypes(include=["datetime"]).columns.tolist()
    )

    return {
        "numerical": numerical_columns,
        "categorical": categorical_columns,
        "datetime": datetime_columns
    }