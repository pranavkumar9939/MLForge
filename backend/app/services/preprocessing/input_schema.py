"""
Builds the "input schema" used to render a single-prediction form on the
frontend: the RAW columns a user should fill in (before one-hot encoding,
scaling, or datetime expansion) - not the post-preprocessing feature list.

This is intentionally separate from `preprocessing_result["feature_names"]`,
which describes the encoded/expanded columns the model actually consumes.
"""

MAX_CATEGORICAL_OPTIONS = 30


def build_input_schema(df, analysis) -> list[dict]:
    target_column = analysis["target_column"]
    schema = []

    for column, info in analysis["column_analysis"].items():

        if column == target_column:
            continue
        if info["is_identifier"] or info.get("is_constant"):
            continue

        col_type = info["type"]  # Numerical | Categorical | Boolean | Datetime
        field = {
            "name": column,
            "type": col_type,
        }

        series = df[column]

        if col_type == "Numerical":
            non_null = series.dropna()
            field["example"] = float(non_null.median()) if len(non_null) else 0
            field["min"] = float(non_null.min()) if len(non_null) else None
            field["max"] = float(non_null.max()) if len(non_null) else None

        elif col_type in ("Categorical", "Boolean"):
            uniques = series.dropna().unique().tolist()
            if len(uniques) <= MAX_CATEGORICAL_OPTIONS:
                field["options"] = [str(u) for u in uniques]
            field["example"] = str(uniques[0]) if uniques else ""

        elif col_type == "Datetime":
            field["example"] = None  # rendered as a date picker on the frontend

        schema.append(field)

    return schema
