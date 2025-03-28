from fastapi import FastAPI
import logging

from app.chroma_utils import is_relevant_query, populate_vector_db
from app.db_utils import create_chat_logs_table
from app.models import QueryInput, QueryOutput

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize
app = FastAPI(
    title="RAG 챗봇",
    description="스마트스토어에 관련 질문에 대한 답변을 제공하는 챗봇입니다.",
)
# populate_vector_db()
# create_chat_logs_table()

@app.post("/chat", response_model=QueryOutput)
def chat(query: QueryInput):
    session_id = query.session_id
    question = query.question

    # Check the relevance of the question to the SmartStore
    if not is_relevant_query(query=question):
        answer = "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다."
    else:
        answer = ""
    # Retrieve the answer from the database
    
    return QueryOutput(session_id=session_id, answer=answer)