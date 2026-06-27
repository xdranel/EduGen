from collections import Counter
from dataclasses import dataclass
from statistics import median

from edugen.ai.data.dataset_manager import DatasetRecord


@dataclass(frozen=True)
class DatasetProfile:
    total_samples: int
    average_length: float
    median_length: float
    longest_sample: int
    shortest_sample: int
    vocabulary_size: int
    token_distribution: list[int]
    recommended_max_tokens: int
    top_words: list[tuple[str, int]]


def profile_records(records: list[DatasetRecord]) -> DatasetProfile:
    lengths = [len(_tokens(record)) for record in records]
    word_counts = Counter(token.lower() for record in records for token in _tokens(record))
    if not lengths:
        return DatasetProfile(0, 0.0, 0.0, 0, 0, 0, [], 512, [])

    sorted_lengths = sorted(lengths)
    percentile_index = min(len(sorted_lengths) - 1, int(len(sorted_lengths) * 0.95))
    recommended = max(256, sorted_lengths[percentile_index])

    return DatasetProfile(
        total_samples=len(records),
        average_length=sum(lengths) / len(lengths),
        median_length=float(median(lengths)),
        longest_sample=max(lengths),
        shortest_sample=min(lengths),
        vocabulary_size=len(word_counts),
        token_distribution=lengths,
        recommended_max_tokens=recommended,
        top_words=word_counts.most_common(20),
    )


def _tokens(record: DatasetRecord) -> list[str]:
    return f"{record.instruction} {record.input} {record.output}".split()
