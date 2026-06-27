from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratedMaterial:
    topic: str
    content: str
    prompt: str
    elapsed_seconds: float
