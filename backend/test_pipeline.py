import pandas as pd

from app.services.preprocessing.column_selector import get_column_groups

from app.services.preprocessing.pipeline_builder import build_preprocessing_pipeline

df = pd.read_csv("uploads/smartcart_customers.csv")

column_groups = get_column_groups(df)

pipeline = build_preprocessing_pipeline(column_groups)

print(pipeline)