import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from edugen.ai.data.dataset_downloader import DatasetDownloader
from edugen.ai.data.pipeline import DataPipeline, DataPipelineConfig
from edugen.ai.data.recommendations import recommended_datasets
from edugen.ai.data.splitter import split_records
from edugen.ai.data.validator import DatasetValidator
from edugen.ai.data.dataset_manager import DatasetRecord


class DataPipelineTest(unittest.TestCase):
    def test_recommended_datasets_are_open_and_reproducible(self) -> None:
        datasets = recommended_datasets()

        self.assertGreaterEqual(len(datasets), 4)
        self.assertTrue(all(dataset.license for dataset in datasets))
        self.assertIn("allenai/sciq", {dataset.dataset_id for dataset in datasets})

    def test_validator_detects_quality_problems(self) -> None:
        records = [
            DatasetRecord(instruction="Explain AI", output="AI is useful."),
            DatasetRecord(instruction="Explain AI", output="AI is useful."),
            DatasetRecord(instruction="", output="missing instruction"),
            DatasetRecord(instruction="short", output="x"),
        ]

        problems = DatasetValidator(min_length=10, max_length=50).validate(records)

        self.assertTrue(any(problem.kind == "duplicate" for problem in problems))
        self.assertTrue(any(problem.kind == "missing_instruction" for problem in problems))
        self.assertTrue(any(problem.kind == "too_short" for problem in problems))

    def test_split_records_uses_deterministic_80_10_10_split(self) -> None:
        records = [
            DatasetRecord(instruction=f"Instruction {index}", output=f"Output {index}")
            for index in range(20)
        ]

        split = split_records(records, seed=7)

        self.assertEqual(len(split.train), 16)
        self.assertEqual(len(split.validation), 2)
        self.assertEqual(len(split.test), 2)

    def test_pipeline_writes_processed_data_metadata_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "sample.json").write_text(
                json.dumps(
                    [
                        {
                            "instruction": "Explain machine learning",
                            "output": "Machine learning uses data to learn patterns.",
                        },
                        {
                            "instruction": "Create a quiz about AI",
                            "output": "Question: What does AI mean? Answer: Artificial intelligence.",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            result = DataPipeline(DataPipelineConfig(root_dir=root)).run()

            self.assertEqual(result.statistics.total_samples, 2)
            self.assertTrue((root / "processed" / "dataset.jsonl").exists())
            self.assertTrue((root / "metadata" / "dataset_info.json").exists())
            self.assertTrue((root / "metadata" / "quality_report.md").exists())

    def test_downloader_verifies_checksum_and_extracts_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_file = root / "inside.txt"
            source_file.write_text("dataset sample", encoding="utf-8")
            archive = root / "sample.zip"
            with zipfile.ZipFile(archive, "w") as zip_file:
                zip_file.write(source_file, arcname="inside.txt")

            checksum = DatasetDownloader.sha256(archive)
            downloaded = DatasetDownloader(root / "downloads").download(
                archive.as_uri(),
                checksum=checksum,
                extract=True,
            )

            self.assertTrue((downloaded / "inside.txt").exists())


if __name__ == "__main__":
    unittest.main()
