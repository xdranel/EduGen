import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExperimentResult:
    name: str
    model_id: str
    parameters: dict[str, float | int | str]
    metrics: dict[str, float]


class ExperimentTracker:
    def __init__(self, output_dir: Path = Path("outputs/evaluation")) -> None:
        self.output_dir = output_dir

    def save(self, result: ExperimentResult) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / "experiments.jsonl"
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")
        return path

    def load(self) -> list[ExperimentResult]:
        path = self.output_dir / "experiments.jsonl"
        if not path.exists():
            return []
        return [
            ExperimentResult(**json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
