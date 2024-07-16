import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
# print(parent, root)
sys.path.append(str(root))


from typing import Any
from fastapi import APIRouter

import pandas as pd
from app import __version__, schemas
from app.config import settings
from fastapi.encoders import jsonable_encoder
from app.schemas.user_query import PredictionResults

from qna_model import __version__ as version_number
from qna_model.src.data_loader import DatasetLoader
from qna_model.src.qa_chain import rag_model
from qna_model.sts_predict import sts_predict_score
from qna_model.pipeline import run_pipeline
from qna_model.sts_pipeline import run_sts_pipeline
from qna_model.gpt_comparision import gpt_model

api_router = APIRouter()

@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, version_number=version_number
    )

    return health.dict()

@api_router.post("/train_sbert")
async def train():
    return run_sts_pipeline()

@api_router.post("/add_to_vectordb")
async def vectorstore():
    return run_pipeline()
    
def row_to_dict(row: pd.Series) -> schemas.ResponseObj:
    try:
        # Create ResponseObj instance with appropriate data types
        res = schemas.ResponseObj(
            question=row["question"],
            student_answer=row["user_input"],
            llm_answer=row["llm_answer"],
            result= row["result"],
            score= row["score"],  # Ensure score is a float
            feedback= row["feedback"]
        )
        return res
    except (KeyError, ValueError) as e:  # Handle potential missing data or type errors
        print(f"Error converting row: {row.to_dict()}. Exception: {e}")
        
def extract_result(message: str): 
    # print("\n...........", type(message.content), "\nFeedback" in str(message.content))
    if "\nFeedback" in str(message):
        return [s.split(":")[1].strip() if "Answer:" in s else s.strip() for s in message.split("\nFeedback:")]
    else:
        return message    
    
@api_router.post("/validate_answers", response_model=schemas.PredictionResults)
async def validate_answers(input_data: schemas.MultipleDataInputs):
    rm = rag_model()
    pred_obj = sts_predict_score()
    gpt_obj = gpt_model()
    
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))
    input_df['llm_answer'] = None
    input_df['score'] = None 
    input_df['result'] = None 
    input_df['feedback'] = None 
    
    # print(input_df.head())
    # print("calling llm to get answers")
    
    # Get LLM Answer
    questions = input_df['question'].values.tolist()
    llm_answers, errors = rm.get_llm_answers(questions)
    
    print(llm_answers, errors)
    if not errors is None:
        return {"predictions": [],"version": version_number, "errors": errors}
    
    for index, row in input_df.iterrows():
        if row['question'] == llm_answers[index][0]:
            row['llm_answer'] = llm_answers[index][1]
    # print(llm_answers)

    # Compare using sbert and gpt
    for index, row in input_df.iterrows():
        q1 = row['question']
        s1 = row['user_input']
        s2 = row['llm_answer']
        
        score = pred_obj.predict(s1, s2) #SBERT Comparision
        print(round(float(score), 4))
        
        message_content = gpt_obj.compare_sentences(q1, s1, s2) #GPT Comparision
        answer, feedback = extract_result(message_content)
        print(f"answer => {answer}, feedback => {feedback}" )
        
        input_df.loc[index, 'score']  = round(score, 4)
        input_df.loc[index, 'result'] = answer
        input_df.loc[index, 'feedback'] =feedback
        
    # print(input_df)
    data_list = input_df.apply(row_to_dict, axis=1).tolist()
    print(data_list)
    # return {"predictions": data_list,"version": version_number, "errors": errors}
    return PredictionResults(predictions=data_list, version=version_number, errors=errors)


# @api_router.get("/getquestions", response_model= Any)
# async def getquestions():
#     dl = DatasetLoader()
#     test_df = dl.load_xlsx_dataset(dl.mastersheet_location)
#     random_rows = test_df.sample(5)
#     response = random_rows['Question'].to_list()
#     return response
