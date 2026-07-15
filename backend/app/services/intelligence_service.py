import pandas as pd

from app.services.intelligence.datatype_detector import detect_column_type
from app.services.intelligence.quality_checker import analyze_quality
from app.services.intelligence.recommendation_engine import generate_recommendations

# def analyze_column_types(df):

#     """
#     Determining the type of column
#     """

    # numerical_columns = []
    # categorical_columns = []
    # boolean_columns = []
    # date_time_columns = []
    # id_columns = []

    # for column in df.columns:

    #     # seperating numerical columns

    #     if pd.api.types.is_numeric_dtype(df[column]):
    #         numerical_columns.append(column)

    #     # seperating boolean columns

    #     elif pd.api.types.is_bool_dtype(df[column]):
    #         boolean_columns.append(column)

    #     # seperating date time coloumns
    #     elif pd.api.types.is_datetime64_any_dtype(df[column]):
    #         date_time_columns.append(column)

    #     # categorical or object columns
    #     else:
    #         categorical_columns.append(column)

    #     # detect possible ID columns
    #     if(
    #         "id" in column.lower() 
    #         or df[column].nunique()==len(df)
    #     ):
    #         id_columns.append(column)


    #     return {
    #         "numerical_columns": numerical_columns,
    #         "categorical_columns": categorical_columns,
    #         "boolean_columns": boolean_columns,
    #         "datetime_columns": date_time_columns,
    #         "id_columns": id_columns
    #     }



def get_column_types(series):
    """
    Determining the logical type of a column
    """

    if pd.api.types.is_bool_dtype(series):
        return "Boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "Numerical"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "DateTime"

    return "Categorical"


def analyze_columns(df):
    """
    Analyze every column in the dataset.
    """

    analysis = {}
    #print(df.columns.tolist())
    quality = analyze_quality(df)
    #print(quality.keys())

    for column in df.columns:

        series = df[column]

        column_info = {
            "dtype": str(series.dtype),
            "type": detect_column_type(series),

            **quality[column]
        }

        column_info["recommendations"] = generate_recommendations(column_info)

        analysis[column] = column_info

    return analysis
