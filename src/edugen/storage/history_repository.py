from dataclasses import dataclass
from pathlib import Path

from edugen.storage.sqlite import get_connection


@dataclass(frozen=True)
class HistoryRecord:
    topic: str
    difficulty: str
    language: str
    content: str
    created_at: str
    id: int | None = None


class HistoryRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def add(self, record: HistoryRecord) -> None:
        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO generation_history
                    (topic, difficulty, language, content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    record.topic,
                    record.difficulty,
                    record.language,
                    record.content,
                    record.created_at,
                ),
            )

    def list(self, limit: int = 50) -> list[HistoryRecord]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, topic, difficulty, language, content, created_at
                FROM generation_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def search(self, query: str, limit: int = 50) -> list[HistoryRecord]:
        pattern = f"%{query}%"
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, topic, difficulty, language, content, created_at
                FROM generation_history
                WHERE topic LIKE ? OR content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (pattern, pattern, limit),
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def delete(self, record_id: int | None) -> None:
        if record_id is None:
            return
        with get_connection(self.database_path) as connection:
            connection.execute("DELETE FROM generation_history WHERE id = ?", (record_id,))

    def _from_row(self, row: tuple[object, ...]) -> HistoryRecord:
        return HistoryRecord(
            id=int(row[0]),
            topic=str(row[1]),
            difficulty=str(row[2] or ""),
            language=str(row[3] or ""),
            content=str(row[4]),
            created_at=str(row[5]),
        )
