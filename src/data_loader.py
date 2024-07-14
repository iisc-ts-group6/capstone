import pandas as pd
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import random
import os
from sklearn.model_selection import train_test_split
from config import DATASET_PATH, SBERT_DATASET_PATH, SBERT_TRAIN_DS, SBERT_TEST_DS, SBERT_EVAL_DS, MATERSHEET_FILEPATH


class DatasetLoader:
    def __init__(self):
        # self.data_path = "data/bio_dataset/csv/"
        self.docs = []
        self.dataset_location = os.path.join(os.getcwd(), DATASET_PATH)
        self.sbert_dataset_location = os.path.join(os.getcwd(), SBERT_DATASET_PATH)
        self.train_ds_location = os.path.join(os.getcwd(), SBERT_TRAIN_DS)
        self.eval_ds_location = os.path.join(os.getcwd(), SBERT_EVAL_DS)
        self.test_ds_location = os.path.join(os.getcwd(), SBERT_TEST_DS)
        self.mastersheet_location = os.path.join(os.getcwd(), MATERSHEET_FILEPATH)
        # print(self.dataset_location)
    
    def load_pdfs(self, pdf_paths: list):
        loaders = []
        for file_path in pdf_paths:
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.exists(full_path):
                loaders.append(PyPDFLoader(full_path))
        docs = []
        for loader in loaders:
            documents = loader.load()
            docs.extend(documents)        
    
        return docs
    
    def load_dataset(self, path='') -> pd.DataFrame:
        if path == '':
            return pd.read_csv(self.dataset_location)
        return pd.read_csv(path)

    def load_xlsx_dataset(self, path='') -> pd.DataFrame:
        if path == '':
            return pd.read_excel(self.sbert_dataset_location)
        return pd.read_excel(self.sbert_dataset_location)
    
    def save_df(self, df: pd.DataFrame, path):
        if not os.path.exists(path):
            df.to_csv(path, index=False)
    
    def load_documents(self) -> list:
        text_loader = TextLoader(self.dataset_location)
        docs_text = text_loader.load()
        self.docs.extend(docs_text)
        return self.docs
    
    def split_dataset(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42):
        train, test = train_test_split(dataframe, test_size=test_size, random_state=random_state)
        return train, test
    
    def train_test_split_and_save(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42):
        train, eval, test = self.train_eval_test_split(dataframe, test_size=test_size, random_state=random_state)
        self.save_df(train, self.train_ds_location)
        self.save_df(eval, self.eval_ds_location)
        self.save_df(test, self.test_ds_location)
        return train, eval, test
    
    def train_eval_test_split(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42, eval_size=0.5):
        train_df, temp_df = train_test_split(dataframe, test_size=test_size, random_state=random_state)
        eval_df, test_df = train_test_split(temp_df, test_size=eval_size, random_state=random_state)
        return train_df, eval_df, test_df
    
    def get_random_question(self):
        df = self.load_dataset()
        random_index = random.randint(0, len(df) - 1)
        question = df.iloc[random_index][0]
        return question

