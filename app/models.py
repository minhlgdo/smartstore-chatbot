from pydantic import BaseModel

class QueryInput(BaseModel):
    session_id: str
    question: str

class QueryOutput(BaseModel):
    session_id: str
    answer: str