from fastapi import FastAPI
import uvicorn
from src.schemas import PredictionResults
from src.qa_chain import rag_model
from pydantic import BaseModel

app = FastAPI()

class UserQuery(BaseModel):
  query: str
  user_input: str

@app.post("/predict", response_model=PredictionResults)
async def predict(data: UserQuery):
  rm = rag_model()
  response = rm.get_llm_answer(query=data.query)
  # data.llm_answer = llm_answer
  return response


# Run the API server (modify host and port if needed)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
