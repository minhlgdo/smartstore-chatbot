import chromadb
import pickle
from app.configs import EMBEDDING_MODEL, FAQ_DATA_PATH
from app.main import openai_client

chromadb_client = chromadb.Client()
collection = chromadb_client.get_or_create_collection("smartstore_faq")

def compute_embedding(text: str):
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def populate_vector_db():
    with open(FAQ_DATA_PATH, "rb") as f:
        data = pickle.load(f)
    
    for question, answer in data.items():
        embedding = compute_embedding(question)
        document = f"Q: {question}\nA: {answer}"
        collection.add(
            embeddings=[embedding],
            documents=[document],
            metadatas=[question]
        )
    