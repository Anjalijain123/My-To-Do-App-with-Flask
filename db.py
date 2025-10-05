import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("TODO_DB", "todo.db")

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(""" CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)""")

if __name__== "__main__":
    init_db()
    print("Initialized DB at ", DB_PATH)


