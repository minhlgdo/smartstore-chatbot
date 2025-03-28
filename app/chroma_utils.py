import logging
import chromadb
import pickle
from app.variables import EMBEDDING_MODEL, FAQ_DATA_PATH
from app.openai_client import client
from chromadb.config import Settings
import tiktoken

chromadb_client = chromadb.PersistentClient(
    path="./chroma", settings=Settings(allow_reset=True)
)
collection = chromadb_client.get_or_create_collection("smartstore_faq")

# Set up logging
logging.basicConfig(level=logging.INFO)

def compute_embedding(text: str):
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def clean_text(text: str) -> str:
    res = text.replace(
        """

위 도움말이 도움이 되었나요?


별점1점

별점2점

별점3점

별점4점

별점5점



소중한 의견을 남겨주시면 보완하도록 노력하겠습니다.

보내기""",
        "",
    )
    res = res.replace("도움말 닫기", "")

    return res


def populate_vector_db():
    with open(FAQ_DATA_PATH, "rb") as f:
        data = pickle.load(f)

    for idx, (question, answer) in enumerate(data.items()):
        # Clean the answer part
        _answer = clean_text(answer)

        document = f"Q: {question}\nA: {_answer}"
        embedding = compute_embedding(document)
        metadata = {"id": str(idx), "question": question}
        collection.upsert(
            embeddings=[embedding],
            documents=[document],
            ids=[str(idx)],
            metadatas=[metadata],
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