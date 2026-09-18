import pandas as pd

data = pd.read_csv("s10_run.csv")

print("CSV loaded successfully!")
print()
print("Columns:")
print(data.columns.tolist())

print()
print("First 5 rows:")
print(data.head())