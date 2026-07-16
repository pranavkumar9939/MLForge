from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def build_numerical_transformer():

    transformer = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(strategy="median")
            ),

            (
                "scaler",
                StandardScaler()
            )

        ]
    )

    return transformer


def build_categorical_transformer():

    transformer = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),

            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore")
            )
        ]

    )

    return transformer