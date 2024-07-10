from pydantic import BaseModel
from typing import Any, List, Optional

class PredictionResults(BaseModel):
    question: str
    answer: str
    errors: Optional[Any]
