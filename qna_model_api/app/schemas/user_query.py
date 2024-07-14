from pydantic import BaseModel

class UserQuery(BaseModel):
  query: str
  user_input: str