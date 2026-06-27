import sqlite3
import tempfile
import unittest
from pathlib import Path

from edugen.config.settings import AppSettings
from edugen.core.validation import validate_topic
from edugen.storage.sqlite import initialize_database


class FoundationTest(unittest.TestCase):
    def test_app_settings_has_project_identity(self) -> None:
        settings = AppSettings()

        self.assertEqual(settings.app_name, "EduGen AI")
        self.assertEqual(settings.version, "0.1.0")

    def test_validate_topic_rejects_empty_text(self) -> None:
        with self.assertRaises(ValueError):
            validate_topic("   ")

    def test_initialize_database_creates_history_table(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "edugen.db"

            initialize_database(db_path)

            with sqlite3.connect(db_path) as connection:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }

        self.assertIn("generation_history", tables)


if __name__ == "__main__":
    unittest.main()
