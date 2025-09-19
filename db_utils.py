import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
def get_db_connection():
    conn = sqlite3.connect('user_data/users.db')
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            embedding_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
