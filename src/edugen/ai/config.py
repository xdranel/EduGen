from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    model_id: str = "Qwen/Qwen2.5-0.5B-Instruct"
    revision: str = "main"
    license: str = "apache-2.0"
    cache_dir: Path = Path("models/cache")
    device: str = "auto"
    torch_dtype: str = "auto"
    trust_remote_code: bool = False


@dataclass(frozen=True)
class GenerationConfig:
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    max_new_tokens: int = 1200
    repetition_penalty: float = 1.1
    do_sample: bool = True
    seed: int | None = 42


@dataclass(frozen=True)
class DatasetConfig:
    root_dir: Path = Path("datasets")
    min_length: int = 10
    max_length: int = 8000
    encoding: str = "utf-8"


@dataclass(frozen=True)
class TrainingConfig:
    output_dir: Path = Path("models/checkpoints")
    method: str = "lora"
    learning_rate: float = 2e-4
    epochs: int = 3
    batch_size: int = 1
    gradient_accumulation_steps: int = 8
    early_stopping_patience: int = 2
