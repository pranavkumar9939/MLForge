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

    unique_values = df[target_column].nunique()

    if unique_values <= 20:
        return "Classification"

    return "Regression"

