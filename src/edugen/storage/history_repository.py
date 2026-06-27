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
