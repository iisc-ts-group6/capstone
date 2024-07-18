import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import pandas as pd
from datasets import load_dataset
from langchain_community.document_loaders import PyPDFLoader
import os, random
from sklearn.model_selection import train_test_split

from qna_model.config import DATASET_PATH, SBERT_TEST_DS,  HF_DATASET_PATH


class DatasetLoader:
    def __init__(self):
        print("inside dataset loader constructor")
        self.docs = []
        self.dataset_location = os.path.join(os.getcwd(), DATASET_PATH)
        # self.sbert_dataset_location = os.path.join(os.getcwd(), SBERT_DATASET_PATH)
        # self.train_ds_location = os.path.join(os.getcwd(), SBERT_TRAIN_DS)
        # self.eval_ds_location = os.path.join(os.getcwd(), SBERT_EVAL_DS)
        self.test_ds_location = os.path.join(os.getcwd(), SBERT_TEST_DS)
        # self.mastersheet_location = os.path.join(os.getcwd(), MATERSHEET_FILEPATH)
        # print(self.dataset_location)
    
    # def load_pdfs(self, pdf_paths: list):
    def load_pdfs(self, pdf_directory: str):
        docs = []
        for filename  in os.listdir(pdf_directory):
            full_path = os.path.join(pdf_directory, filename)
            if os.path.exists(full_path):
                try:
                    loader = PyPDFLoader(full_path)
                    docs.extend(loader.load()) 
                except Exception as e:    
                    print(f'Error in reading file: {full_path}')
        return docs
    
    def load_dataset(self, path='') -> pd.DataFrame:
        if path == '':
            return pd.read_csv(self.dataset_location)
        return pd.read_csv(path)

    # def load_sbert_dataset(self, path='') -> pd.DataFrame:
    #     if path == '':
    #         return pd.read_csv(self.sbert_dataset_location)
    #     return pd.read_csv(path)
    
    def save_df(self, df: pd.DataFrame, path):
        # print(path)
        # if os.path.exists(path):
        #     os.remove(path)
        df.to_csv(path, index=False, mode='w')
    
    # def load_documents(self) -> list:
    #     text_loader = TextLoader(self.dataset_location)
    #     docs_text = text_loader.load()
    #     self.docs.extend(docs_text)
    #     return self.docs
    
    def split_dataset(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42):
        train, test = train_test_split(dataframe, test_size=test_size, random_state=random_state)
        return train, test
    
    # def train_test_split_and_save(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42):
    #     print("inside train_test_split_and_save")
    #     train, eval, test = self.train_eval_test_split(dataframe, test_size=test_size, random_state=random_state)
    #     print(self.train_ds_location)
    #     self.save_df(train, self.train_ds_location)
    #     self.save_df(eval, self.eval_ds_location)
    #     self.save_df(test, self.test_ds_location)
    #     print("train_test_split_and_save is Done!")
    #     return train, eval, test
    
    def load_hf_dataset(self, split_name="train"):
        # ds = load_dataset(HF_DATASET_PATH)
        # or load the separate splits if the dataset has train/validation/test splits
        train_dataset = load_dataset(HF_DATASET_PATH, split=split_name) 
        return train_dataset.to_pandas()
        
    
    def train_eval_test_split(self, dataframe: pd.DataFrame, test_size=0.2, random_state=42, eval_size=0.5):
        train_df, temp_df = train_test_split(dataframe, test_size=test_size, random_state=random_state)
        eval_df, test_df = train_test_split(temp_df, test_size=eval_size, random_state=random_state)
        return train_df, eval_df, test_df
    
    def get_random_questions(self, datafile, num=5):
        questions = []
        try:
                
            print(datafile)
            ds2 = load_dataset(path=HF_DATASET_PATH, data_files=datafile)
            questions = ds2['train']['Question']
        except Exception as e:
            print(e)
            questions = []
            
        if datafile == "" or len(questions) < num:
            print('loading from test')
            ds = load_dataset(HF_DATASET_PATH, split="test")
            questions = ds['Question']
            
        print(f"total questions = {len(questions)}")
        # random_index = random.randint(0, len(df) - 1)
        # sample_df = df.to_pandas().sample(n=num)
        questions =[str(s).strip() for s in random.sample(questions, num)]
        return questions

