from pydantic import BaseModel

class QueryInput(BaseModel):
    session_id: str
    question: str
