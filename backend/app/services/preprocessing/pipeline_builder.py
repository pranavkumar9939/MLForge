from sklearn.compose import ColumnTransformer

from app.services.preprocessing.transformer_builder import (
    build_numerical_transformer,
    build_categorical_transformer
)

def build_preprocessing_pipeline(column_groups):
    """
    Create a preprocessing pipeline for the dataset
    """

    numerical_columns = column_groups["numerical"]
    categorical_columns = column_groups["categorical"]

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "numerical",
                build_numerical_transformer(),
                numerical_columns,
            ),

            (
                "categorical",
                build_categorical_transformer(),
                categorical_columns,
            ),
        ],

        remainder="drop"
    )

    return preprocessor