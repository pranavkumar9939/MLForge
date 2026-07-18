def analyze_quality(df):
    """
    Analyze dataset quality and identify potential issues.
    """

    quality = {}

    IDENTIFIER_KEYWORDS = [
        "id",
        "uuid",
        "guid",
        "roll",
        "rollno",
        "roll_number",
        "registration",
        "regno",
        "passport",
        "invoice",
        "transaction",
        "orderid",
        "customerid"
    ]

    for column in df.columns:

        series = df[column]

        unique = series.nunique()

        column_name = column.lower().replace("-","_")

        tokens = column_name.split("_")

        is_identifier = (
            column in IDENTIFIER_KEYWORDS
            or any(
                token in IDENTIFIER_KEYWORDS
                for token in tokens
            )
        )

        print(
            column,
            "| unique =", unique,
            "| rows =", len(df),
            "| identifier =", is_identifier
        )

        quality[column] = {
            "missing": int(series.isnull().sum()),
            "Missing_percentage": round(series.isnull().mean() * 100, 2),
            "unique": int(unique),
            "is_constant": unique <= 1,
            "is_identifier":is_identifier
        }

    for col, info in quality.items():
        print(col, info["unique"], info["is_identifier"])

    return quality


    