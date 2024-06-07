import pandas as pd

# Loading SciEntsBank to a dataframe

df = pd.read_parquet('data/data-SciEntsBank/train-00001.parquet')
print(df.shape)

