import pandas as pd

def analyze_dataset(file_path):
    """
        Reads a csv file and returns basic dataset statics.
    """

    df = pd.read_csv(file_path)

    analysis = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_mb": round(
            df.memory_usage(deep = True).sum() / (1024*1024), 2
        )
    }

    return analysis