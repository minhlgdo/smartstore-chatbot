from fastapi import FastAPI
import logging

from app.chroma_utils import populate_vector_db
from app.db_utils import create_chat_logs_table

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize
app = FastAPI(
    title="RAG 챗봇",
    description="스마트스토어에 관련 질문에 대한 답변을 제공하는 챗봇입니다.",
)
populate_vector_db()
create_chat_logs_table()

@app.get("/chat")
async def root():
    return {"message": "Hello World"}