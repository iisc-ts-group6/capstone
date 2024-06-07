import pandas as pd

def load_dataset(loc: str) -> pd.DataFrame:
    return pd.read_parquet(loc)

loc = 'data/data-SciEntsBank/train-00001.parquet'
df = load_dataset(loc)
print('Dataset shape : ', df.shape)


