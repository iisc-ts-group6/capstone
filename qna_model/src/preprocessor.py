import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import pandas as pd

from qna_model.config import CHUNK_SIZE, CHUNK_OVERLAP

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )
    return text_splitter.split_documents(docs)

def clean_text(text: str):
    # Remove excess newline characters
    text = re.sub(r'\s+', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def fill_none_values(df):
    # Clean the data to ensure no NaN values
    df.fillna("", inplace=True)


def preprocess_docs(docs: list):
    # Clean the data to ensure no NaN values
    
    return docs

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Clean the data to ensure no NaN values
    fill_none_values(df)
    # Apply text cleaning to each column
    for col in df.columns:
        if df[col].dtype == "str":
            df[col] = df[col].apply(clean_text)      
    return df
