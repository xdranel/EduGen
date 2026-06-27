from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationMetrics:
    output_length: int
    word_count: int
    latency_seconds: float


def basic_generation_metrics(text: str, latency_seconds: float) -> GenerationMetrics:
    return GenerationMetrics(
        output_length=len(text),
        word_count=len(text.split()),
        latency_seconds=latency_seconds,
    )
