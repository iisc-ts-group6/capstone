from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import pandas as pd
from config import CHUNK_SIZE, CHUNK_OVERLAP


class Preprocessor:
    def __init__(self):
        pass

    def split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(docs)
        return splits

    def clean_text(self, text):
        # Remove excess newline characters
        text = re.sub(r'\s+', ' ', text)
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    def preprocess_data(self, df):
        # Clean the data to ensure no NaN values
        df.fillna("", inplace=True)
        # Apply text cleaning to each column
        df['question'] = df['Question'].apply(self.clean_text)
        df['answer'] = df['Answer'].apply(self.clean_text)
        df['D1'] = df['D1'].apply(self.clean_text)
        df['D2'] = df['D2'].apply(self.clean_text)
        df['D3'] = df['D3'].apply(self.clean_text)
        return df
