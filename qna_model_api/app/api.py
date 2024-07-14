from fastapi import FastAPI
import uvicorn
from src.schemas import PredictionResults
from src.qa_chain import rag_model
import sts_predict as pred
from pydantic import BaseModel
from typing import Any

from src.data_loader import DatasetLoader

app = FastAPI()

class UserQuery(BaseModel):
  query: str
  user_input: str

@app.post("/predict", response_model= Any)
async def predict(data: UserQuery):
    rm = rag_model()
    question = data.query
    result = rm.get_llm_answer(query=question)
    print(result)
    student_answer = data.user_input
    llm_answer = result['answer']
    
    print(student_answer)
    print(llm_answer)
    score = pred.predict(llm_answer, student_answer)
    print(score)
    response = { 'question': question , 'student_answer': student_answer , 
                 'llm_answer':llm_answer , 'score': str(score)}
    return response

@app.get("/getquestions", response_model= Any)
async def getquestions():
    dl = DatasetLoader()
    test_df = dl.load_xlsx_dataset(dl.mastersheet_location)
    random_rows = test_df.sample(5)
    response = random_rows['Question'].to_list()
    return response

# Run the API server (modify host and port if needed)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
     
