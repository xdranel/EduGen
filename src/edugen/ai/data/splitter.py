from dataclasses import dataclass
import random

from edugen.ai.data.dataset_manager import DatasetRecord


@dataclass(frozen=True)
class DatasetSplit:
    train: list[DatasetRecord]
    validation: list[DatasetRecord]
    test: list[DatasetRecord]


def split_records(
    records: list[DatasetRecord],
    train_ratio: float = 0.8,
    validation_ratio: float = 0.1,
    seed: int = 42,
) -> DatasetSplit:
    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    train_end = int(len(shuffled) * train_ratio)
    validation_end = train_end + int(len(shuffled) * validation_ratio)
    return DatasetSplit(
        train=shuffled[:train_end],
        validation=shuffled[train_end:validation_end],
        test=shuffled[validation_end:],
    )
