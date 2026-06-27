from dataclasses import dataclass

from edugen.ai.data.dataset_manager import DatasetRecord


@dataclass(frozen=True)
class ValidationProblem:
    index: int
    kind: str
    message: str


class DatasetValidator:
    def __init__(self, min_length: int = 10, max_length: int = 8000) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, records: list[DatasetRecord]) -> list[ValidationProblem]:
        problems: list[ValidationProblem] = []
        seen: set[tuple[str, str]] = set()

        for index, record in enumerate(records):
            combined = f"{record.instruction} {record.output}".strip()
            key = (record.instruction, record.output)

            if not record.instruction.strip():
                problems.append(ValidationProblem(index, "missing_instruction", "Instruction is empty."))
            if not record.output.strip():
                problems.append(ValidationProblem(index, "missing_output", "Output is empty."))
            if key in seen:
                problems.append(ValidationProblem(index, "duplicate", "Duplicate instruction/output pair."))
            if len(combined) < self.min_length:
                problems.append(ValidationProblem(index, "too_short", "Sample is shorter than minimum length."))
            if len(combined) > self.max_length:
                problems.append(ValidationProblem(index, "too_long", "Sample is longer than maximum length."))

            try:
                combined.encode("utf-8").decode("utf-8")
            except UnicodeError:
                problems.append(ValidationProblem(index, "encoding", "Sample is not valid UTF-8."))

            seen.add(key)

        return problems
