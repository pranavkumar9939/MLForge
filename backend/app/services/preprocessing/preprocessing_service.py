import pandas as pd
from scipy import sparse
from sklearn.preprocessing import LabelEncoder

from app.services.preprocessing.pipeline_builder import build_preprocessing_pipeline
from app.services.preprocessing.datetime_features import expand_datetime_column


def preprocess_dataset(df: pd.DataFrame, analysis: dict) -> dict:
    """
    Automatically preprocess the dataset.

    - Numerical columns: median impute + scale.
    - Categorical AND Boolean columns: most-frequent impute + one-hot encode.
    - Datetime columns: expanded into numeric components (year/month/day/
      day-of-week/quarter/weekend/hour) rather than being silently dropped.
    - Identifier columns and the target column are excluded, and every
      excluded column is recorded with a reason (no silent drops).
    - Classification targets are label-encoded (fit on the full target
      column - this is safe, it is not a feature and cannot leak
      information between train/test splits the way feature scaling would).
    """

    df = df.copy()

    target_column = analysis["target_column"]
    problem_type = analysis["problem_type"]

    # Rows with a missing target cannot be used for training or evaluation -
    # there is no label to learn from or measure against. Drop them here
    # (not silently: the count is reported in the summary) rather than
    # letting them corrupt label encoding or metrics downstream.
    rows_before = len(df)
    df = df[df[target_column].notna()].reset_index(drop=True)
    rows_dropped_missing_target = rows_before - len(df)

    numerical_columns = []
    categorical_columns = []
    dropped_columns = []

    for column, info in analysis["column_analysis"].items():

        if column == target_column:
            continue

        if info["is_identifier"]:
            dropped_columns.append({
                "column": column,
                "reason": "Detected as an identifier column (e.g. ID, UUID) which carries no predictive signal",
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

    column_groups = {
        "numerical": numerical_columns,
        "categorical": categorical_columns,
    }

    pipeline = build_preprocessing_pipeline(column_groups)

    feature_columns = numerical_columns + categorical_columns
    X = df[feature_columns]
    y_raw = df[target_column]

    # Capture a small, bounded set of observed categories per categorical
    # column so a prediction form can offer a dropdown instead of free text.
    # Capped to avoid bloating metadata for high-cardinality columns.
    categorical_options = {}
    for col in categorical_columns:
        values = df[col].dropna().astype(str).unique().tolist()
        if len(values) <= 50:
            categorical_options[col] = sorted(values)

    numerical_ranges = {}
    for col in numerical_columns:
        series = df[col].dropna()
        if len(series):
            numerical_ranges[col] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": round(float(series.mean()), 4),
            }

    label_encoder = None
    if problem_type in ("Binary Classification", "Multi-Class Classification", "Multilabel Classification"):
        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y_raw), index=y_raw.index, name=target_column)
    else:
        y = y_raw

    X_processed = pipeline.fit_transform(X)

    if sparse.issparse(X_processed):
        processed_df = pd.DataFrame.sparse.from_spmatrix(
            X_processed,
            columns=pipeline.get_feature_names_out(),
        )
    else:
        processed_df = pd.DataFrame(
            X_processed,
            columns=pipeline.get_feature_names_out(),
        )

    return {
        "X": X_processed,
        "y": y,
        "pipeline": pipeline,
        "label_encoder": label_encoder,
        "feature_names": pipeline.get_feature_names_out(),
        "preprocessed_dataframe": processed_df,
        "summary": {
            "target_column": target_column,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "categorical_options": categorical_options,
            "numerical_ranges": numerical_ranges,
            "dropped_columns": dropped_columns,
            "rows_dropped_missing_target": rows_dropped_missing_target,
            "input_features": len(numerical_columns) + len(categorical_columns),
            "output_features": X_processed.shape[1],
        },
    }
