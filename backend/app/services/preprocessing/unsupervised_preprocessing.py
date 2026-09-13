"""
Preprocessing for unsupervised workflows (clustering, dimensionality
reduction), which have no target column. Mirrors `preprocessing_service.py`
but without any target-handling logic.
"""

import pandas as pd
from scipy import sparse

from app.services.intelligence_service import analyze_columns
from app.services.preprocessing.pipeline_builder import build_preprocessing_pipeline
from app.services.preprocessing.datetime_features import expand_datetime_column


def preprocess_unsupervised(df: pd.DataFrame) -> dict:
    df = df.copy()
    column_analysis = analyze_columns(df)

    numerical_columns = []
    categorical_columns = []
    dropped_columns = []

    for column, info in column_analysis.items():

        if info["is_identifier"]:
            dropped_columns.append({
                "column": column,
                "reason": "Detected as an identifier column, which carries no clustering signal",
            })
            continue

        if info.get("is_constant"):
            dropped_columns.append({
                "column": column,
                "reason": "Column has a single constant value across all rows",
            })
            continue

        col_type = info["type"]

        if col_type == "Numerical":
            numerical_columns.append(column)
        elif col_type == "Boolean":
            categorical_columns.append(column)
        elif col_type == "Datetime":
            df, new_cols = expand_datetime_column(df, column)
            numerical_columns.extend(new_cols)
        elif col_type == "Categorical":
            categorical_columns.append(column)
        else:
            dropped_columns.append({
                "column": column,
                "reason": f"Unrecognized column type '{col_type}'",
            })

    if len(numerical_columns) + len(categorical_columns) < 2:
        raise ValueError(
            "At least two usable feature columns are required for clustering "
            "or dimensionality reduction after excluding identifiers and constants."
        )

    column_groups = {"numerical": numerical_columns, "categorical": categorical_columns}
    pipeline = build_preprocessing_pipeline(column_groups)

    feature_columns = numerical_columns + categorical_columns
    X = df[feature_columns]

    X_processed = pipeline.fit_transform(X)
    if sparse.issparse(X_processed):
        X_processed = X_processed.toarray()

    return {
        "X": X_processed,
        "pipeline": pipeline,
        "feature_names": pipeline.get_feature_names_out(),
        "summary": {
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "dropped_columns": dropped_columns,
            "input_features": len(numerical_columns) + len(categorical_columns),
            "output_features": X_processed.shape[1],
        },
    }
