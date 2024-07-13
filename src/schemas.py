from pydantic import BaseModel
from typing import Any, List, Optional

class PredictionResults(BaseModel):
    question: str
    llm_answer: str
    student_answer: str
    score: float
    errors: Optional[Any]
