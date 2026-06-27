from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class HumanEvaluationForm:
    correctness: int
    coherence: int
    readability: int
    educational_value: int
    completeness: int
    grammar: int
    relevance: int

    def average_score(self) -> float:
        scores = asdict(self).values()
        return sum(scores) / len(asdict(self))

    def validate(self) -> None:
        for name, value in asdict(self).items():
            if value < 1 or value > 5:
                raise ValueError(f"{name} must be between 1 and 5.")
