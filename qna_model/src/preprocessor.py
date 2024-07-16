import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import pandas as pd
from itertools import product 

from qna_model.config import CHUNK_SIZE, CHUNK_OVERLAP


def convert_to_pairs(df: pd.DataFrame)-> pd.DataFrame:
    """Converts all rows of a dataframe into multiple pairs for training.

    Args:
        df: A pandas dataframe with the specified columns:
            - 'Answer': Main answer text
            - 'Para1', 'Para2': Columns with positive examples
            - 'D1', 'D2', 'D3': Columns with distractor examples

    Returns:
        A pandas DataFrame with columns "Sentence1", "Sentence2", and "Label".
        "Label" values are 1 for pairs from pos_pairs else 0.
    """
    all_pairs = []
    for _, row in df.iterrows():  # Iterate through rows efficiently
        answer = row['Answer']
        positive_columns = row[['Para1','Para2']]
        distractor_columns = row[['D1','D2','D3']]

        # Generate positive pairs (1 for pos_pairs)
        pos_pairs = product([answer], positive_columns.values.tolist())
        pos_pairs = [(str(pair[0]), str(pair[1]), 1.0) for pair in pos_pairs]

        # Generate negative pairs (0 for neg_pairs)
        neg_pairs = product([answer], distractor_columns.values.flatten().tolist())
        neg_pairs = [(str(pair[0]), str(pair[1]), 0) for pair in neg_pairs]
        
        all_pairs.extend(list(pos_pairs))
        all_pairs.extend(list(neg_pairs))

    # Create a DataFrame with the specified columns
    pairs_df = pd.DataFrame(all_pairs, columns=['Sentence1', 'Sentence2', 'Label'])
    return pairs_df
    
  
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


# def preprocess_docs(docs: list):
#     # Clean the data to ensure no NaN values
    
#     return docs

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Clean the data to ensure no NaN values
    fill_none_values(df)
    # Apply text cleaning to each column
    for col in df.columns:
        if df[col].dtype == "str":
            df[col] = df[col].apply(clean_text)      
    return df
