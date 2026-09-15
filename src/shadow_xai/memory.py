"""Privacy-aware SQLite conversation memory."""

from dataclasses import asdict, dataclass
import json
import sqlite3
import time


@dataclass(frozen=True)
class MemoryItem:
    id: int
    user_id: str
    role: str
    content: str
    created_at: float


class MemoryStore:
    def __init__(self, path: str = ":memory:") -> None:
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, user_id TEXT, role TEXT, content TEXT, created_at REAL)")
        self.db.commit()

    def add(self, user_id: str, role: str, content: str) -> int:
        cur = self.db.execute("INSERT INTO memories(user_id,role,content,created_at) VALUES(?,?,?,?)", (user_id, role, content, time.time()))
        self.db.commit()
        return int(cur.lastrowid)

    def recent(self, user_id: str, limit: int = 20) -> list[MemoryItem]:
        rows = self.db.execute("SELECT id,user_id,role,content,created_at FROM memories WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()
        return [MemoryItem(*row) for row in reversed(rows)]

    def search(self, user_id: str, query: str, limit: int = 5) -> list[MemoryItem]:
        terms = [f"%{term}%" for term in query.split() if term]
        if not terms:
            return []
        where = " OR ".join("content LIKE ?" for _ in terms)
        rows = self.db.execute(f"SELECT id,user_id,role,content,created_at FROM memories WHERE user_id=? AND ({where}) ORDER BY id DESC LIMIT ?", (user_id, *terms, limit)).fetchall()
        return [MemoryItem(*row) for row in rows]

    def delete_user(self, user_id: str) -> None:
        self.db.execute("DELETE FROM memories WHERE user_id=?", (user_id,)); self.db.commit()

    def export_user(self, user_id: str) -> str:
        return json.dumps([asdict(x) for x in self.recent(user_id, 100000)], ensure_ascii=False, indent=2)

    def close(self) -> None:
        self.db.close()
