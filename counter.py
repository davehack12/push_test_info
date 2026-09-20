import sqlite3, threading
from config import DB_PATH, LIMIT

_lock = threading.Lock()

def _conn():
    c = sqlite3.connect(DB_PATH)
    c.execute("""CREATE TABLE IF NOT EXISTS counts (
        user_id  TEXT PRIMARY KEY,
        n        INTEGER NOT NULL DEFAULT 0,
        notified INTEGER NOT NULL DEFAULT 0
    )""")
    return c

def increment(user_id: str) -> tuple[int, int]:
    """Returns (count, notified). Count never exceeds LIMIT."""
    with _lock:
        c = _conn()
        row = c.execute("SELECT n, notified FROM counts WHERE user_id = ?",
                        (str(user_id),)).fetchone()
        n, notified = (row if row else (0, 0))

        if n < LIMIT:
            n += 1
        c.execute(
            "INSERT INTO counts(user_id, n, notified) VALUES(?,?,?) "
            "ON CONFLICT(user_id) DO UPDATE SET n=excluded.n, notified=excluded.notified",
            (str(user_id), n, notified)
        )
        c.commit()
        c.close()
        return n, notified

def mark_notified(user_id: str) -> None:
    with _lock:
        c = _conn()
        c.execute("UPDATE counts SET notified = 1 WHERE user_id = ?", (str(user_id),))
        c.commit()
        c.close()
