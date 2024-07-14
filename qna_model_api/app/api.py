import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
# print(parent, root)
sys.path.append(str(root))


from typing import Any
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app import __version__, schemas
from app.config import settings
from qna_model import __version__ as version_number
from qna_model.src.data_loader import DatasetLoader
from qna_model.src.qa_chain import rag_model
from qna_model.sts_predict import sts_predict_score


api_router = APIRouter()

class UserQuery(BaseModel):
  query: str
  user_input: str

@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, version_number=version_number
    )

    return health.dict()


@api_router.post("/predict", response_model= Any)
async def predict(data: UserQuery):
    rm = rag_model()
    question = data.query
    result = rm.get_llm_answer(query=question)
    print(result)
    student_answer = data.user_input
    llm_answer = result['answer']
    
    print(student_answer)
    print(llm_answer)
    pred_obj = sts_predict_score()
    score = pred_obj.predict(llm_answer, student_answer)
    print(score)
    response = { 'question': question , 'student_answer': student_answer , 
                 'llm_answer':llm_answer , 'score': str(score)}
    return response

@api_router.get("/getquestions", response_model= Any)
async def getquestions():
    dl = DatasetLoader()
    test_df = dl.load_xlsx_dataset(dl.mastersheet_location)
    random_rows = test_df.sample(5)
    response = random_rows['Question'].to_list()
    return response
