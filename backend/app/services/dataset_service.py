import pandas as pd

from app.services.intelligence_service import analyze_columns
from app.services.problem_detector import (
    detect_target_column,
    detect_problem_type
)


def analyze_dataset(df):
    """
        Reads a csv file and returns basic dataset statics.
    """

    df = df

    print("\n===== COLUMN DATA TYPES =====")

    for column in df.columns:
        print(column, "------>", df[column].dtype)

    print("=============================\n")

    column_details = analyze_columns(df)

    target_column = detect_target_column(df)
    problem_type = detect_problem_type(df, target_column)

    analysis = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_mb": round(
            df.memory_usage(deep = True).sum() / (1024*1024), 2
        ),

        "column_analysis": column_details,

        "problem_type": problem_type,
        "target_column": target_column
    }

    return analysis