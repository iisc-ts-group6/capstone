from pydantic import BaseModel
from typing import Any, List, Optional

class UserQuery(BaseModel):
  question: str
  user_input: str

class ResponseObj(BaseModel):
  question: str
  student_answer: str
  llm_answer: str
  gpt_answer: str
  result: str
  score: float
      

class MultipleDataInputs(BaseModel):
    inputs: List[UserQuery]

class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[ResponseObj]]
