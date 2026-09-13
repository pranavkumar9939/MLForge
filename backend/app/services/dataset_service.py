import pandas as pd

from app.services.intelligence_service import analyze_columns
from app.services.problem_detector import (
    recommend_target_columns,
    detect_problem_type,
)


def analyze_dataset(df: pd.DataFrame, target_column: str | None = None) -> dict:
    """
    Reads a dataframe and returns dataset statistics, column analysis, and
    a target-column recommendation.

    IMPORTANT: if `target_column` is not supplied, the analysis returns a
    recommendation only (`analysis["target_column"]` will be the top
    suggestion, but `analysis["target_confirmed"]` will be False and
    `analysis["target_recommendation"]["requires_confirmation"]` will be
    True). Callers that go on to preprocess/train MUST NOT do so on an
    unconfirmed target without surfacing that fact to the user.
    """

    column_details = analyze_columns(df)

    recommendation = recommend_target_columns(df)

    target_confirmed = target_column is not None and target_column in df.columns
    resolved_target = target_column if target_confirmed else recommendation["recommended_column"]

    problem_type = None
    if resolved_target is not None:
        problem_type = detect_problem_type(df, resolved_target)

    analysis = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_mb": round(
            df.memory_usage(deep=True).sum() / (1024 * 1024), 2
        ),

        "column_analysis": column_details,

        "problem_type": problem_type,
        "target_column": resolved_target,
        "target_confirmed": target_confirmed,
        "target_recommendation": recommendation,
    }

    return analysis
