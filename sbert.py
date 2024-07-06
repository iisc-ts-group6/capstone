from dotenv import load_dotenv
from config import SBERT_MODEL_NAME
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
import pandas as pd
from src.sbert_model import SBERTModel
from sentence_transformers import SentenceTransformer

def run_pipeline():
    
    #1. Load configurations
    load_dotenv()
    
    st = SBERTModel()
    pp = Preprocessor()
    dl = DataLoader()
    
    #2. load dataset
    qna_dataset = dl.load_dataset()
    print(qna_dataset.shape)
    
    #3. split dataset into train, test
    train_df, test_df = dl.split_dataset(qna_dataset, test_size=0.2)
    print(train_df.shape, test_df.shape)
    ##### start training process ######
    #4. Preprocess like cleanup, fill empty values, etc 
    train_data = pp.preprocess_data(train_df)
    # print(train_data.info())
    #5. Convert train dataset into triplets <Q, A, L> pairs
    train_qna_pairs = st.create_examples(train_data)
    #6. Finetune pre-trained model and save the metrics
    st.fine_tune(train_qna_pairs)
    # Calculate and save evaluation metrics after fine-tuning
    evaluation_result = st.evaluate(train_qna_pairs)
    print(evaluation_result)
    ##### end training process ######

    #7. Evaulate and get metrics
    test_data = st.preprocess_data(test_df)
    test_qna_pairs = st.create_examples(test_data)
    sbert_evaluation_result = st.evaluate(test_qna_pairs, phase="eval_test")
    print(sbert_evaluation_result)


if __name__ == "__main__":
    run_pipeline()    
    