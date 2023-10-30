import pandas as pd

df = pd.read_parquet("./data/pet_dataset.parquet")

print(df.head())
