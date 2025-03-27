from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_MODEL = "gpt-4o-mini"
FAQ_DATA_PATH = "assets/final_result.pkl"
