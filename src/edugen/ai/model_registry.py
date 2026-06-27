from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRecommendation:
    model_id: str
    license: str
    size: str
    reason: str
    source_url: str


RECOMMENDED_MODEL = ModelRecommendation(
    model_id="Qwen/Qwen2.5-0.5B-Instruct",
    license="apache-2.0",
    size="0.5B parameters",
    reason=(
        "Best first local model for this project: small enough for student "
        "hardware, instruction-tuned, Transformers-compatible, permissive "
        "license, and configurable for later replacement."
    ),
    source_url="https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct",
)


SUPPORTED_MODELS = {
    RECOMMENDED_MODEL.model_id: RECOMMENDED_MODEL,
    "HuggingFaceTB/SmolLM2-1.7B-Instruct": ModelRecommendation(
        model_id="HuggingFaceTB/SmolLM2-1.7B-Instruct",
        license="apache-2.0",
        size="1.7B parameters",
        reason="Good small alternative when more memory is available.",
        source_url="https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct",
    ),
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0": ModelRecommendation(
        model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        license="apache-2.0",
        size="1.1B parameters",
        reason="Very small baseline model, but weaker educational generation quality.",
        source_url="https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    ),
}
