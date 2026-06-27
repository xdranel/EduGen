import json
from dataclasses import dataclass
from pathlib import Path

from edugen.ai.config import DatasetConfig
from edugen.ai.data.dataset_manager import DatasetManager, DatasetRecord
from edugen.ai.data.metadata import dataclass_to_dict, write_json
from edugen.ai.data.quality_report import build_quality_report
from edugen.ai.data.recommendations import recommended_datasets
from edugen.ai.data.splitter import DatasetSplit, split_records
from edugen.ai.data.statistics import DatasetProfile, profile_records
from edugen.ai.data.validator import DatasetValidator, ValidationProblem
from edugen.ai.data.visualization import write_length_distribution


@dataclass(frozen=True)
class DataPipelineConfig:
    root_dir: Path = Path("datasets")
    seed: int = 42
    train_ratio: float = 0.8
    validation_ratio: float = 0.1
    min_length: int = 10
    max_length: int = 8000


@dataclass(frozen=True)
class DataPipelineResult:
    records: list[DatasetRecord]
    split: DatasetSplit
    statistics: DatasetProfile
    problems: list[ValidationProblem]


class DataPipeline:
    def __init__(self, config: DataPipelineConfig | None = None) -> None:
        self.config = config or DataPipelineConfig()

    @classmethod
    def from_dataset_config(cls, config: DatasetConfig) -> "DataPipeline":
        return cls(
            DataPipelineConfig(
                root_dir=config.root_dir,
                min_length=config.min_length,
                max_length=config.max_length,
            )
        )

    def run(self) -> DataPipelineResult:
        self._ensure_structure()
        records = DatasetManager(self.config.root_dir / "raw").load_all()
        validator = DatasetValidator(self.config.min_length, self.config.max_length)
        problems = validator.validate(records)
        statistics = profile_records(records)
        split = split_records(
            records,
            train_ratio=self.config.train_ratio,
            validation_ratio=self.config.validation_ratio,
            seed=self.config.seed,
        )

        self._write_records(records, self.config.root_dir / "processed" / "dataset.jsonl")
        self._write_records(split.train, self.config.root_dir / "train" / "dataset.jsonl")
        self._write_records(split.validation, self.config.root_dir / "validation" / "dataset.jsonl")
        self._write_records(split.test, self.config.root_dir / "test" / "dataset.jsonl")
        self._write_metadata(statistics, split, problems)
        write_length_distribution(statistics.token_distribution, Path("outputs/statistics"))

        return DataPipelineResult(records, split, statistics, problems)

    def _ensure_structure(self) -> None:
        for name in [
            "raw",
            "processed",
            "train",
            "validation",
            "test",
            "metadata",
            "cache",
            "statistics",
            "downloads",
        ]:
            (self.config.root_dir / name).mkdir(parents=True, exist_ok=True)

    def _write_records(self, records: list[DatasetRecord], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(json.dumps(record.__dict__, ensure_ascii=False) + "\n")

    def _write_metadata(
        self,
        statistics: DatasetProfile,
        split: DatasetSplit,
        problems: list[ValidationProblem],
    ) -> None:
        metadata_dir = self.config.root_dir / "metadata"
        write_json(
            metadata_dir / "dataset_info.json",
            {
                "recommended_split": "80/10/10",
                "split_reason": "Good default for small to medium supervised fine-tuning datasets.",
                "sources": [dataset.__dict__ for dataset in recommended_datasets()],
            },
        )
        write_json(metadata_dir / "statistics.json", dataclass_to_dict(statistics))
        write_json(
            metadata_dir / "preprocessing_log.json",
            {"steps": ["load", "clean", "deduplicate", "validate", "split", "metadata"]},
        )
        write_json(
            metadata_dir / "source_information.json",
            {"sources": [dataset.__dict__ for dataset in recommended_datasets()]},
        )
        write_json(
            metadata_dir / "split_metadata.json",
            {
                "train": len(split.train),
                "validation": len(split.validation),
                "test": len(split.test),
                "seed": self.config.seed,
            },
        )
        write_json(
            metadata_dir / "validation_problems.json",
            [problem.__dict__ for problem in problems],
        )
        (metadata_dir / "quality_report.md").write_text(build_quality_report(problems), encoding="utf-8")
