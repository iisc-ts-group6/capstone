# Prerequisite 
# pip install pyarrow

import pandas as pd

def load_dataset(loc: str, doc_type: str):
    if doc_type == 'par': # parquet
        return pd.read_parquet(loc)
    elif doc_type == 'pdf':
        return True # code pending. return a doc object

loc = 'data/data-SciEntsBank/train-00001.parquet'
doc_type = 'par'
df = load_dataset(loc, doc_type)
print('Dataset shape : ', df.shape)




