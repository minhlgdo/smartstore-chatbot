import chromadb
import pickle
from app.variables import EMBEDDING_MODEL, FAQ_DATA_PATH
from app.openai_client import client

chromadb_client = chromadb.PersistentClient(path="./chroma_db")
collection = chromadb_client.get_or_create_collection("smartstore_faq")

def compute_embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def populate_vector_db():
    with open(FAQ_DATA_PATH, "rb") as f:
        data = pickle.load(f)
    
    for idx, (question, answer) in enumerate(data.items()):
        document = f"Q: {question}\nA: {answer}"
        embedding = compute_embedding(document)
        metadata = {"id": str(idx), "question": question}
        collection.add(
            embeddings=[embedding],
            documents=[document],
            ids=[str(idx)],
            metadatas=[metadata]
        )

def is_relevant_query(query: str, threshold: float = 0.3) -> bool:
    """
    Check the relevance of the query against the FAQ data stored in the vector store.
    Returns True if the best matching FAQ question has a distance below the threshold.
    """
    embedding = compute_embedding(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        include=["distances"]  # ensure distances are returned
    )

    if "distances" in results and results["distances"]:
        best_distance = results["distances"][0][0]
        print(f"Best distance: {best_distance}")
        return best_distance < threshold
    
    return False