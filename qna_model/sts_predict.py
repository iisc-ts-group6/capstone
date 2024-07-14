import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from qna_model.src.sbert_model import SBERTModel
from qna_model.src.data_loader import DatasetLoader
import qna_model.src.preprocessor as pp
from qna_model.config import HF_FINTUNE_MODEL_PATH

st = SBERTModel()

class sts_predict_score:
    def __init__(self) -> None:
        self.model = st.load_model(HF_FINTUNE_MODEL_PATH)
        
    def predict(self, sentence1: str, sentence2: str):
        # question = pp.clean_text(question)
        correct_answer = pp.clean_text(sentence1)
        student_answer = pp.clean_text(sentence2)
        embeddings = self.model.encode([correct_answer, student_answer])
        similarity_score = st.cosine_similarity(embeddings[0], embeddings[1])
        return similarity_score


if __name__ == "__main__":
    dl = DatasetLoader()
    test_df = dl.load_dataset(dl.test_ds_location)
    
    random_row = test_df.sample(n=1)
    sentence1 = random_row['Sentence1'].iloc[0]
    sentence2 = random_row['Sentence2'].iloc[0]
    print( random_row)
    print(f'Label: {random_row["Label"].iloc[0]}')
    pred_obj = sts_predict_score()
    score = pred_obj.predict(sentence1, sentence2)
    print(f'similarity score: {score}')
