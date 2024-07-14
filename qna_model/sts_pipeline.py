#sts_pipeline.py (Semantic Textual Similarity)
import pandas as pd
from itertools import product 
import pandas as pd

from src.sbert_model import SBERTModel
from src.data_loader import DatasetLoader
from config import BATCH_SIZE, EPOCHS, train_test_split_size


def convert_to_pairs(df)-> pd.DataFrame:
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
    
  
def run_sts_pipeline():
    dl = DatasetLoader()
    data = dl.load_sbert_dataset()

    pairs_df = convert_to_pairs(data.copy())
    print('dataset loaded...')
    print(data.shape, pairs_df.shape)
    
    train_df, eval_df, test_df = dl.train_test_split_and_save(pairs_df, test_size=train_test_split_size, random_state=42)
    print(train_df.shape, eval_df.shape, test_df.shape)
    print('split and saving train and test dataset complete')

    # pp.preprocess_data(train_df)
    
    # Load pre-trained SBERT model  all-mpnet-base-v2 or all-MiniLM-L6-v2
    st = SBERTModel()
    st.fine_tune(train_df, epochs=EPOCHS, batch_size=BATCH_SIZE)
    
    # Calculate and save evaluation metrics after fine-tuning
    evaluation_result = st.evaluate(eval_df)
    print(evaluation_result)
    
if __name__ == "__main__":
    run_sts_pipeline()
