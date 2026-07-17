import pandas as pd
from scipy import sparse

# from app.services.preprocessing.column_selector import get_column_groups
from app.services.preprocessing.pipeline_builder import build_preprocessing_pipeline
# from app.services.problem_detector import detect_target_column


def preprocess_dataset(df, analysis):
    """
    Automatically preprocess the dataset.
    """

    numerical_columns = []
    categorical_columns = []

    for column, info in analysis["column_analysis"].items():

        if info["is_identifier"]:
            continue

        if column == analysis["target_column"]:
            continue

        if info["type"] == "Numerical":
            numerical_columns.append(column)

        elif info["type"] == "Categorical":
            categorical_columns.append(column)

    column_groups = {
        "numerical": numerical_columns,
        "categorical": categorical_columns
    }

    pipeline = build_preprocessing_pipeline(column_groups)

    target_column = analysis["target_column"]

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_processed = pipeline.fit_transform(X)

    print(type(X_processed))
    print(X_processed.shape)
    print(len(pipeline.get_feature_names_out()))
    print("Numerical:", numerical_columns)
    print("Categorical:", categorical_columns)
    if sparse.issparse(X_processed):

        processed_df = pd.DataFrame.sparse.from_spmatrix(
            X_processed,
            columns=pipeline.get_feature_names_out()
        )

    else:

        processed_df = pd.DataFrame(
            X_processed,
            columns=pipeline.get_feature_names_out()
        )

    return {
        "X": X_processed,
        "y": y,
        "pipeline": pipeline,
        "feature_names": pipeline.get_feature_names_out(),
        "preprocessed_dataframe": processed_df,
        "summary": {
            "target_column": target_column,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "input_features": len(numerical_columns) + len(categorical_columns),
            "output_features": X_processed.shape[1]
        }
    }




    