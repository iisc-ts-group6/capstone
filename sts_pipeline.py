#sts_pipeline.py (Semantic Textual Similarity)

import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from datetime import datetime
from itertools import product 
import pandas as pd
import torch

from src.data_loader import DatasetLoader
from config import sts_model_name, BATCH_SIZE, EPOCHS, train_test_split_size, SBERT_TRAIN_DS, SBERT_TEST_DS

# specify GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)


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
        pos_pairs = [(pair[0], pair[1], 1) for pair in pos_pairs]

        # Generate negative pairs (0 for neg_pairs)
        neg_pairs = product([answer], distractor_columns.values.flatten().tolist())
        neg_pairs = [(pair[0], pair[1], 0) for pair in neg_pairs]
        
        all_pairs.extend(list(pos_pairs))
        all_pairs.extend(list(neg_pairs))

    # Create a DataFrame with the specified columns
    return pd.DataFrame(all_pairs, columns=['Sentence1', 'Sentence2', 'Label'])
    
# Function to convert DataFrame to InputExample objects
def convert_df_to_input_examples(df):
    examples = []
    for _, row in df.iterrows():
        sentence1 = row['Sentence1']
        sentence2 = row['Sentence2']
        label = row['Label']        
        examples.append(InputExample(texts=[sentence1, sentence2], label=label))
    return examples

def df_to_input_examples(df):
    pairs = df[['Sentence1', 'Sentence2']]
    labels = df['Label']
    examples = [InputExample(texts=[pair[0], pair[1]], label=label) for pair, label in zip(pairs, labels)]
    return examples

def run_sts_pipeline():
    dl = DatasetLoader()
    data = dl.load_xlsx_dataset()
    pairs_df = convert_to_pairs(data.copy())
    print('dataset loaded...')
    print(data.shape, pairs_df.shape)
    
    train_df, test_df = dl.split_dataset(pairs_df, test_size=train_test_split_size, random_state=42)
    
    #save train and test data
    dl.save_df(train_df, dl.train_ds_location)
    dl.save_df(test_df, dl.test_ds_location)
    print('split dataset complete')

    # Convert DataFrames to InputExample format
    # train_examples = convert_df_to_input_examples(train_df)
    # test_examples = convert_df_to_input_examples(test_df)
    train_examples =  df_to_input_examples(train_df)
    test_examples =  df_to_input_examples(test_df)
     
    
    # Load pre-trained SBERT model  all-mpnet-base-v2 or all-MiniLM-L6-v2
    model = SentenceTransformer(sts_model_name)
    print(f'loaded pre-trained model: {sts_model_name}')

    # Define our training loss and a DataLoader for training
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)
    train_loss = losses.CosineSimilarityLoss(model=model)
    
    # Fine-tune the model
    warmup_steps = 50
    print('training started....')
    model.fit(train_objectives=[(train_dataloader, train_loss)],
            epochs=EPOCHS,
            warmup_steps=warmup_steps,
            show_progress_bar=True)
    
    # Save the fine-tuned model
    model_save_path = '.models/finetuned_sbert_model'
    model.save(model_save_path)
    print(f"model saved at {model_save_path}")

if __name__ == "__main__":
    run_sts_pipeline()
