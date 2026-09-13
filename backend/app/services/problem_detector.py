"""
Target-column recommendation and problem-type detection.

IMPORTANT: `detect_target_column` never silently commits to a choice when
there is real ambiguity. It always returns a *recommendation* plus the full
ranked list of candidates with reasons, so the caller (API/UI) can show the
user a suggestion and let them confirm or override it. The actual target
used for training must come from an explicit `target_column` value that
either the user chose or that was accepted from the recommendation.
"""

import pandas as pd

COMMON_TARGET_NAMES = [
    "target", "label", "class", "output", "response", "outcome",
    "price", "salary", "churn", "fraud", "survived", "purchased",
    "approved", "result", "diagnosis", "y",
]

ID_TOKENS = ["id", "uuid", "guid", "index", "no", "number"]


def _score_column(df: pd.DataFrame, column: str) -> dict:
    """Score a single column as a target candidate. Higher = more likely target."""
    series = df[column]
    n_rows = len(df)
    unique = series.nunique(dropna=True)
    name = column.lower().replace("-", "_")
    tokens = name.split("_")

    score = 0.0
    reasons = []

    if name in COMMON_TARGET_NAMES or any(t in COMMON_TARGET_NAMES for t in tokens):
        score += 40
        reasons.append("Column name matches a common target-variable pattern")

    if any(t in ID_TOKENS for t in tokens):
        score -= 50
        reasons.append("Column name suggests an identifier, unlikely to be a target")

    if unique == n_rows and n_rows > 1:
        score -= 40
        reasons.append("Every value is unique, which is typical of an identifier column, not a target")

    if pd.api.types.is_numeric_dtype(series):
        if 1 < unique <= 20:
            score += 15
            reasons.append("Numeric column with a small number of distinct values (classification-like)")
        elif unique > 20:
            score += 10
            reasons.append("Continuous numeric column (regression-like)")
    else:
        if 1 < unique <= 20:
            score += 20
            reasons.append("Categorical column with a small number of classes")

    if column == df.columns[-1]:
        score += 10
        reasons.append("Column is the last column in the dataset (common convention)")

    if series.isnull().mean() > 0.3:
        score -= 15
        reasons.append("Column has a high proportion of missing values")

    if unique <= 1:
        score -= 100
        reasons.append("Column is constant and cannot be a useful target")

    return {
        "column": column,
        "score": round(score, 2),
        "unique_values": int(unique),
        "dtype": str(series.dtype),
        "reasons": reasons,
    }


def recommend_target_columns(df: pd.DataFrame) -> dict:
    """
    Return a ranked list of target-column candidates with scores and reasons.
    Does NOT choose one for the caller - it only recommends.
    """
    candidates = [_score_column(df, col) for col in df.columns]
    candidates.sort(key=lambda c: c["score"], reverse=True)

    top = candidates[0] if candidates else None
    # Ambiguous if the top two candidates are close in score, or the top score is low.
    ambiguous = True
    if top is not None:
        second_score = candidates[1]["score"] if len(candidates) > 1 else -999
        ambiguous = (top["score"] - second_score) < 10 or top["score"] < 15

    return {
        "recommended_column": top["column"] if top else None,
        "confidence": "low" if ambiguous else "high",
        "requires_confirmation": True,  # always require explicit user confirmation
        "candidates": candidates,
    }


def detect_target_column(df: pd.DataFrame) -> str:
    """
    Backwards-compatible convenience wrapper that returns only the top
    recommendation. Callers that need to train a model should NOT rely on
    this silently - they should go through `recommend_target_columns` and
    require explicit confirmation from the user first.
    """
    return recommend_target_columns(df)["recommended_column"]


def detect_problem_type(df: pd.DataFrame, target_column: str) -> str:
    """
    Detect the machine learning problem type from the target column.
    """
    target = df[target_column]
    unique_values = target.nunique(dropna=True)

    if pd.api.types.is_numeric_dtype(target):
        if unique_values > 20:
            return "Regression"
        elif unique_values == 2:
            return "Binary Classification"
        else:
            return "Multi-Class Classification"

    if unique_values == 2:
        return "Binary Classification"

    return "Multi-Class Classification"
