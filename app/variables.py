from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_MODEL = "gpt-4o-mini"
FAQ_DATA_PATH = "assets/final_result.pkl"
DB_NAME = "chatbot_db"

# MESSAGES
QUESTION_ERROR_MESSAGE = "챗봇이 후속 질문을 생성하는 중 오류가 발생했습니다. 다시 시도하십시오."
ANSWER_ERROR_MESSAGE = "챗봇이 답변을 생성하는 중 오류가 발생했습니다. 다시 시도하십시오."
