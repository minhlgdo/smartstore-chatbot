import logging
import chromadb
import pickle
from app.text_utils import clean_text, sliding_window_split_text
from app.variables import EMBEDDING_MODEL, FAQ_DATA_PATH
from app.openai_client import client
from chromadb.config import Settings

chromadb_client = chromadb.PersistentClient(
    path="./chroma", settings=Settings(allow_reset=True)
)
collection = chromadb_client.get_or_create_collection(
    name="smartstore_faq", metadata={"hnsw:space": "cosine"}
)

# Set up logging
logging.basicConfig(level=logging.INFO)


def compute_embedding(text: str):
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def populate_vector_db():
    with open(FAQ_DATA_PATH, "rb") as f:
        data = pickle.load(f)

    for data_idx, (question, answer) in enumerate(data.items()):
        # Clean the answer part
        _answer = clean_text(answer)
        document = f"Q: {question}\nA: {_answer}"

        chunks = sliding_window_split_text(document)

        for chunk_idx, chunk in enumerate(chunks):
            embedding = compute_embedding(chunk)
            col_id = f"{data_idx}_{chunk_idx}"
            metadata = {"id": f"{col_id}", "question": question, "chunk_idx": chunk_idx}
            logging.info(f"Adding document id {col_id} to vector DB")

            collection.upsert(
                embeddings=[embedding],
                documents=[chunk],
                ids=[col_id],
                metadatas=[metadata],
            )


def get_relevant_faq(question: str, n_results: int = 3) -> str:
    """
    Retrieve the most relevant FAQ questions from the vector store based on the input question.
    """
    embedding = compute_embedding(question)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["documents"],
    )

    if "documents" in results and results["documents"]:
        documents = results["documents"][0]
        if documents:
            # join the documents into a single string
            return "\n\n".join(documents)
        
    return ""


def is_relevant_query(query: str, threshold: float = 0.45) -> bool:
    """
    Check the relevance of the query against the FAQ data stored in the vector store.
    Returns True if the best matching FAQ question has a distance below the threshold.
    """
    embedding = compute_embedding(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        include=["distances"],  # ensure distances are returned
    )

    if "distances" in results and results["distances"]:
        best_distance = results["distances"][0][0]
        print(f"Best distance: {best_distance}")
        return best_distance < threshold

    return False


if collection.count() == 0:
    logging.info("Populating vector DB with FAQ data...")
    populate_vector_db()
    logging.info("Vector DB populated successfully.")
else:
    logging.info("Vector DB already populated.")
