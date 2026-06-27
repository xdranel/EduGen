import csv
import json
from dataclasses import dataclass
from pathlib import Path

from edugen.ai.preprocessing.cleaner import TextPreprocessor


@dataclass(frozen=True)
class DatasetRecord:
    instruction: str
    output: str
    input: str = ""
    source: str = ""


@dataclass(frozen=True)
class DatasetStatistics:
    total_samples: int
    average_instruction_length: float
    average_output_length: float


class DatasetManager:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.preprocessor = TextPreprocessor()

    def load_all(self) -> list[DatasetRecord]:
        records: list[DatasetRecord] = []
        if not self.root_dir.exists():
            return records

        for path in sorted(self.root_dir.rglob("*")):
            if path.suffix == ".csv":
                records.extend(self.load_csv(path))
            elif path.suffix == ".json":
                records.extend(self.load_json(path))
            elif path.suffix == ".txt":
                records.extend(self.load_txt(path))

        return self.remove_duplicates(records)

    def load_csv(self, path: Path) -> list[DatasetRecord]:
        with path.open(newline="", encoding="utf-8") as file:
            return [self._record_from_mapping(row, path) for row in csv.DictReader(file)]

    def load_json(self, path: Path) -> list[DatasetRecord]:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else [data]
        return [self._record_from_mapping(row, path) for row in rows if isinstance(row, dict)]

    def load_txt(self, path: Path) -> list[DatasetRecord]:
        lines = self.preprocessor.clean_many(path.read_text(encoding="utf-8").splitlines())
        return [DatasetRecord(instruction=line, output="", source=str(path)) for line in lines]

    def validate(self, records: list[DatasetRecord]) -> list[str]:
        problems: list[str] = []
        for index, record in enumerate(records):
            if not record.instruction:
                problems.append(f"record {index}: missing instruction")
            if not record.output and record.source.endswith((".csv", ".json")):
                problems.append(f"record {index}: missing output")
        return problems

    def statistics(self, records: list[DatasetRecord]) -> DatasetStatistics:
        if not records:
            return DatasetStatistics(0, 0.0, 0.0)

        return DatasetStatistics(
            total_samples=len(records),
            average_instruction_length=sum(len(row.instruction) for row in records) / len(records),
            average_output_length=sum(len(row.output) for row in records) / len(records),
        )

    def remove_duplicates(self, records: list[DatasetRecord]) -> list[DatasetRecord]:
        seen: set[tuple[str, str]] = set()
        unique: list[DatasetRecord] = []
        for record in records:
            key = (record.instruction, record.output)
            if key in seen:
                continue
            seen.add(key)
            unique.append(record)
        return unique

    def _record_from_mapping(self, row: dict[str, object], path: Path) -> DatasetRecord:
        instruction = str(row.get("instruction") or row.get("prompt") or row.get("question") or "")
        output = str(row.get("output") or row.get("response") or row.get("answer") or "")
        input_text = str(row.get("input") or row.get("context") or "")
        formatted = self.preprocessor.instruction_format(instruction, output, input_text)
        return DatasetRecord(source=str(path), **formatted)
