from fastapi import FastAPI
from openai import OpenAI
import logging

from app.chroma_utils import populate_vector_db

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize
openai_client = OpenAI()
app = FastAPI()
populate_vector_db()


@app.get("/chat")
async def root():
    return {"message": "Hello World"}