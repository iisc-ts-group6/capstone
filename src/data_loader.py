import pandas as pd
from langchain_community.document_loaders import TextLoader
import random
import os
from sklearn.model_selection import train_test_split
from config import DATASET_PATH


class DataLoader:
    def __init__(self):
        # self.data_path = "data/bio_dataset/csv/"
        self.docs = []
        self.dataset_location = os.path.join(os.getcwd(), DATASET_PATH)
        print(self.dataset_location)
    
    def load_dataset(self) -> pd.DataFrame:
        return pd.read_csv(self.dataset_location)

    def load_documents(self) -> list:
        text_loader = TextLoader(self.dataset_location)
        docs_text = text_loader.load()
        self.docs.extend(docs_text)
        return self.docs
    
    def split_dataset(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42):
        train, test = train_test_split(dataframe, test_size=test_size, random_state=random_state)
        return train, test
    
    def get_random_question(self):
        df = self.load_dataset()
        random_index = random.randint(0, len(df) - 1)
        question = df.iloc[random_index][0]
        return question