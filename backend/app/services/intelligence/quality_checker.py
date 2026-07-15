def analyze_quality(df):
    """
    Analyze dataset quality and identify potential issues.
    """

    quality = {}

    for column in df.columns:

        series = df[column]

        quality[column] = {
            "missing": int(series.isnull().sum()),
            "Missing_percentage": round(
                series.isnull().mean() * 100, 2
            ),
            "unique": int(series.nunique()),
            "is_constant": series.nunique() <= 1,
            "is_identifier": (
                "id" in column.lower() or 
                series.nunique() == len(df)
            ),
        }

    return quality


    