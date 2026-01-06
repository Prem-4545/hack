"""
db_init.py

Create an empty SQLite users database for local development.
"""
import sqlite3

DB = "users.db"

schema = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    email TEXT
);
'''

if __name__ == '__main__':
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript(schema)
    conn.commit()
    conn.close()
    print(f"Initialized {DB}")
