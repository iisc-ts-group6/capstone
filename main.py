# Prerequisite 
# pip install pandas
# pip install langchain
# pip install pypdf
# pip install pyarrow

import pandas as pd
import langchain
from pypdf import PdfReader



def load_dataset(doc_loc: str, doc_type: str):
    if doc_type == 'par': # parquet
        return pd.read_parquet(doc_loc)
    elif doc_type == 'pdf':
        text = ""
        try:
            reader = PdfReader(doc_loc)
            for page in reader.pages:
                text += page.extract_text()
        except Exception as exc:
            print("ERROR: pdf extraction failed") #text = fallback_text_extraction("example.pdf")
        return text 
    return "ERROR: Dataset load failed. Check file type. Only parquet and pdf supported."


doc_loc = 'data/data-SciEntsBank/train-00001.parquet'
doc_type = 'par'
df = load_dataset(doc_loc, doc_type)
print('Parquet dataset shape : ', df.shape)


doc_loc = 'data/10/jesc1an.pdf'
doc_type = 'pdf'
pdf_text = load_dataset(doc_loc, doc_type)
print('PDF dataset :' , pdf_text)



