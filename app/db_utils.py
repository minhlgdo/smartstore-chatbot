import sqlite3
import logging

from app.variables import DB_NAME

logging.basicConfig(level=logging.INFO)


def get_db_connection():
    conn = sqlite3.connect(database=DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_chat_logs_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            chatbot_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def insert_chat_log(session_id: str, user_query: str, chatbot_response: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chat_logs (session_id, user_query, chatbot_response)
        VALUES (?, ?, ?)
    """,
        (session_id, user_query, chatbot_response),
    )
    conn.commit()
    conn.close()


def get_chat_history(session_id: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT user_query, chatbot_response, timestamp
        FROM chat_logs
        WHERE session_id = ?
    """,
        (session_id,),
    )

    messages = []
    for row in cursor.fetchall():
        messages.append(f"유저: {row['user_query']}\n챗봇: {row['chatbot_response']}")

    conn.close()
    return "\n".join(messages)


create_chat_logs_table()
logging.info("Chat logs table created successfully.")