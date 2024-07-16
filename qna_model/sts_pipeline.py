#sts_pipeline.py (Semantic Textual Similarity)
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# import pandas as pd
from src.sbert_model import SBERTModel
from src.data_loader import DatasetLoader
from src.preprocessor import convert_to_pairs
from config import BATCH_SIZE, EPOCHS, train_test_split_size


def run_sts_pipeline():
    dl = DatasetLoader()
    st = SBERTModel()
    
    # print("dl object created")
    # data = dl.load_sbert_dataset()
    # print('dataset loaded...', data.shape)

    # train_df, eval_df, test_df = dl.train_test_split_and_save(data, test_size=train_test_split_size, random_state=42)
    # print(train_df.shape, eval_df.shape, test_df.shape)
    # print('split and saving train and test dataset complete')
    
    # Load from hugging face
    train_df = dl.load_hf_dataset(split_name="train")
    eval_df = dl.load_hf_dataset(split_name="validation")
    print("loaded from hugging face datasets", train_df.shape, eval_df.shape)

    train_pairs_df = convert_to_pairs(train_df.copy())
    eval_pairs_df = convert_to_pairs(eval_df.copy())
    print("convert_to_pairs complete", train_pairs_df.shape, eval_pairs_df.shape)
    
    # pp.preprocess_data(train_df)
    
    # Load pre-trained SBERT model  all-mpnet-base-v2 or all-MiniLM-L6-v2
    st.fine_tune(train_pairs_df, epochs=EPOCHS, batch_size=BATCH_SIZE)
    
    # Calculate and save evaluation metrics after fine-tuning
    evaluation_result = st.evaluate(eval_pairs_df)
    print(evaluation_result)
    
if __name__ == "__main__":
    run_sts_pipeline()
