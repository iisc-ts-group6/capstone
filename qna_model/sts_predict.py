import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from qna_model.src.sbert_model import SBERTModel
from qna_model.src.data_loader import DatasetLoader
import qna_model.src.preprocessor as pp
from qna_model.config import HF_FINTUNE_MODEL_PATH
import pandas as pd
import json

st = SBERTModel()

class sts_predict_score:
    def __init__(self) -> None:
        self.model = st.load_model(HF_FINTUNE_MODEL_PATH)
        
    def predict(self, sentence1: str, sentence2: str) -> float:
        # question = pp.clean_text(question)
        correct_answer = pp.clean_text(sentence1)
        student_answer = pp.clean_text(sentence2)
        embeddings = self.model.encode([correct_answer, student_answer])
        similarity_score = st.cosine_similarity(embeddings[0], embeddings[1])
        return similarity_score

    def compare_answers(self, df: pd.DataFrame):
        df['Score'] = None 
        for index, row in df.iterrows():
            s1 = row['Sentence1']
            s2 = row['Sentence2']
            # print(s1, s2)
            df.loc[index, 'Score']  = self.predict(s1, s2)
        return df

    def row_to_dict(self, row):
        return {
            # "question": row["question"],
            "student_answer": row["Sentence1"],
            "llm_answer": row["Sentence2"],
            "gpt_answer": "",  # Handle missing gpt_answer
            # "result": row["result"],
            "score": str(row["Score"]),  # Convert score to string for JSON
        }

if __name__ == "__main__":
    dl = DatasetLoader()
    test_df = dl.load_dataset(dl.test_ds_location)
    pred_obj = sts_predict_score()
    
    # test1
    # random_row = test_df.sample(n=1)
    # sentence1 = random_row['Sentence1'].iloc[0]
    # sentence2 = random_row['Sentence2'].iloc[0]
    # print( random_row)
    # print(f'Label: {random_row["Label"].iloc[0]}')
    # score = pred_obj.predict(sentence1, sentence2)
    # print(f'similarity score: {score}')
    
    # #test2
    # print("testing multiple sentence comparision.....")
    # rows_to_compare = test_df[['Sentence1', 'Sentence2']].sample(n=5)
    # print(rows_to_compare.shape)
    # cosine_scores = pred_obj.compare_answers(rows_to_compare)
    # print(cosine_scores)

    #test3
    print("testing multiple sentence comparision.....")
    rtc = test_df.sample(n=5)
    df = pred_obj.compare_answers(rtc)
    data_list = df.apply(pred_obj.row_to_dict, axis=1).tolist()
    json_data = json.dumps(data_list)

    print(json_data)