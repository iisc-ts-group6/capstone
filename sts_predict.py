from src.sbert_model import SBERTModel
from src.data_loader import DatasetLoader
import src.preprocessor as pp

st = SBERTModel()

def predict(sentence1: str, sentence2: str):
    model = st.load_model(st.output_model_path)
 
    # question = pp.clean_text(question)
    correct_answer = pp.clean_text(sentence1)
    student_answer = pp.clean_text(sentence2)
    embeddings = model.encode([correct_answer, student_answer])
    similarity_score = st.cosine_similarity(embeddings[0], embeddings[1])
    return similarity_score


if __name__ == "__main__":
    dl = DatasetLoader()
    test_df = dl.load_dataset(dl.test_ds_location)
    
    random_row = test_df.sample(n=1)
    sentence1 = random_row['Sentence1'].iloc[0]
    sentence2 = random_row['Sentence2'].iloc[0]
    # print( sentence1)
    # print( type(sentence1))
    score = predict(sentence1, sentence2)
    print(score)
    # # Access data in the random row (assuming it's a Series)
    # print(random_row.iloc[0])  # Access first element (value)
    # print(random_row.index[0])   # Access index (row label)