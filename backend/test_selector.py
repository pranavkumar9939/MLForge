import pandas as pd

from app.services.preprocessing.column_selector import get_column_groups

df = pd.read_csv("uploads/smartcart_customers.csv")

print(get_column_groups(df))