"""
Automatic datetime feature extraction.

Detected datetime columns are expanded into numeric, model-friendly
components instead of being silently dropped by the preprocessing pipeline.
"""

import pandas as pd


def expand_datetime_column(df: pd.DataFrame, column: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Parse `column` as a datetime and add extracted numeric feature columns
    to `df` (in place on a copy). Returns the modified dataframe and the
    list of newly created feature column names. The original column is
    left untouched by this function - the caller is responsible for
    excluding it from the numerical/categorical column groups.
    """
    parsed = pd.to_datetime(df[column], errors="coerce")

    new_columns = []

    def add(suffix, values):
        name = f"{column}__{suffix}"
        df[name] = values
        new_columns.append(name)

    add("year", parsed.dt.year)
    add("month", parsed.dt.month)
    add("day", parsed.dt.day)
    add("dayofweek", parsed.dt.dayofweek)
    add("quarter", parsed.dt.quarter)
    add("is_weekend", (parsed.dt.dayofweek >= 5).astype(int))

    # Only include time-of-day components if there's actual variation
    # (otherwise every row would show 00:00:00 and add pure noise).
    if parsed.dt.hour.nunique(dropna=True) > 1:
        add("hour", parsed.dt.hour)

    return df, new_columns
