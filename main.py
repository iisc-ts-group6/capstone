import pandas as pd

# Loading SciEntsBank to a dataframe
df_sci_ents = pd.read_parquet('data/data-SciEntsBank/train-00001.parquet')
print("SciEntsBank dataset shape : ", df_sci_ents.shape)

# Loading SciQ dataset to a dataframe
df_sci_q = pd.read_parquet('data/data-SciQ/train-00000-of-00001.parquet')
print("SciQ dataset shape : ", df_sci_q.shape)

