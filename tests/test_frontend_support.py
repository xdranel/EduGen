import tempfile
import unittest
from pathlib import Path

from edugen.exports.document_exporter import DocumentExporter
from edugen.storage.history_repository import HistoryRecord, HistoryRepository
from edugen.storage.sqlite import initialize_database
from edugen.ui.content_parser import split_sections


SAMPLE_CONTENT = """1. Learning Summary
AI studies intelligent systems.

2. Detailed Explanation
Machine learning uses data.

7. Flashcards
Q: What is AI?
A: Artificial intelligence.
"""


class FrontendSupportTest(unittest.TestCase):
    def test_split_sections_extracts_numbered_sections(self) -> None:
        sections = split_sections(SAMPLE_CONTENT)

        self.assertEqual(sections[0].title, "Learning Summary")
        self.assertIn("intelligent systems", sections[0].body)
        self.assertEqual(sections[1].title, "Detailed Explanation")

    def test_document_exporter_generates_text_markdown_and_html(self) -> None:
        exporter = DocumentExporter()

        self.assertIn("Learning Summary", exporter.to_markdown("AI", SAMPLE_CONTENT))
        self.assertIn("AI studies", exporter.to_text("AI", SAMPLE_CONTENT))
        self.assertIn("<html", exporter.to_html("AI", SAMPLE_CONTENT))

    def test_history_repository_lists_searches_and_deletes_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "history.db"
            initialize_database(db_path)
            repository = HistoryRepository(db_path)
            repository.add(
                HistoryRecord(
                    topic="AI",
                    difficulty="Beginner",
                    language="English",
                    content=SAMPLE_CONTENT,
                    created_at="2026-06-27T00:00:00+00:00",
                )
            )

            all_records = repository.list()
            search_results = repository.search("AI")
            repository.delete(all_records[0].id)

            remaining = repository.list()

        self.assertEqual(len(all_records), 1)
        self.assertEqual(search_results[0].topic, "AI")
        self.assertEqual(remaining, [])


if __name__ == "__main__":
    unittest.main()
