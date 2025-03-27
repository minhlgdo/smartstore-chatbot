import sqlite3

from app.variables import DB_NAME

def get_db_connection():
    conn = sqlite3.connect(database=DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def create_chat_logs_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            chatbot_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_chat_log(session_id, user_query, chatbot_response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_logs (session_id, user_query, chatbot_response)
        VALUES (?, ?, ?)
    """, (session_id, user_query, chatbot_response))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_query, chatbot_response, timestamp
        FROM chat_logs
        WHERE session_id = ?
    """, (session_id,))

    messages = []
    for row in cursor.fetchall():
        messages.append([
            {"role": "human", "content": row['user_query']},
            {"role": "chatbot", "content": row['chatbot_response']}
        ])
    conn.close()
    return messages