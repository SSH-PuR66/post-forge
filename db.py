import sqlite3
from contextlib import contextmanager

DB_PATH = "postforge.db"

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS usage (
            ip TEXT NOT NULL,
            day TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (ip, day)
        );
        """)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def token_is_active(token: str) -> bool:
    with get_db() as db:
        row = db.execute(
            "SELECT active FROM tokens WHERE token = ?", (token,)
        ).fetchone()
        return bool(row and row["active"])

def create_token(token: str, customer_id: str):
    with get_db() as db:
        db.execute(
            "INSERT OR IGNORE INTO tokens (token, customer_id) VALUES (?, ?)",
            (token, customer_id),
        )

def deactivate_customer(customer_id: str):
    with get_db() as db:
        db.execute(
            "UPDATE tokens SET active = 0 WHERE customer_id = ?", (customer_id,)
        )

def free_uses_today(ip: str, day: str) -> int:
    with get_db() as db:
        row = db.execute(
            "SELECT count FROM usage WHERE ip = ? AND day = ?", (ip, day)
        ).fetchone()
        return row["count"] if row else 0

def increment_usage(ip: str, day: str):
    with get_db() as db:
        db.execute(
            """INSERT INTO usage (ip, day, count) VALUES (?, ?, 1)
               ON CONFLICT(ip, day) DO UPDATE SET count = count + 1""",
            (ip, day),
        )
