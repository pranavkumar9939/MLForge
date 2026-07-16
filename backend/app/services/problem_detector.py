import pandas as pd

COMMON_TARGETS = [
    "target",
    "label",
    "class",
    "output",
    "response",
    "price",
    "salary",
    "churn",
    "fraud",
    "survived",
    "purchased"
]


def detect_target_column(df):

    # checking for common name targets
    for column in df.columns:

        if column.lower() in COMMON_TARGETS:
            return column

    # last line which should be target
    return df.columns[-1]

def detect_problem_type(df, target_column):
    """
    Detect the machine learning problem type.
    """

    target = df[target_column]

    unique_values = target.nunique()

    # Numerical target
    if pd.api.types.is_numeric_dtype(target):

        # Regression
        if unique_values > 20:
            return "Regression"

        # Binary Classification
        elif unique_values == 2:
            return "Binary Classification"

        # Multi-Class Classification
        else:
            return "Multi-Class Classification"

    # Non-numerical target

    if unique_values == 2:
        return "Binary Classification"

    return "Multi-Class Classification"

