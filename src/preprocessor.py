from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import pandas as pd
from config import CHUNK_SIZE, CHUNK_OVERLAP

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )
    return text_splitter.split_documents(docs)

def clean_text(text):
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
        df[col] = df[col].apply(clean_text)            
    # df['question'] = df['Question'].apply(self.clean_text)
    # df['answer'] = df['Answer'].apply(self.clean_text)
    # df['D1'] = df['D1'].apply(self.clean_text)
    # df['D2'] = df['D2'].apply(self.clean_text)
    # df['D3'] = df['D3'].apply(self.clean_text)
    return df
    

