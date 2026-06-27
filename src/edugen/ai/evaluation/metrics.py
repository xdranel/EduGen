from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
import time


@dataclass(frozen=True)
class GenerationMetrics:
    output_length: int
    word_count: int
    latency_seconds: float
    rouge_1: float = 0.0
    rouge_l: float = 0.0
    bleu: float = 0.0
    bert_score: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    generation_speed_tokens_per_second: float = 0.0


def basic_generation_metrics(text: str, latency_seconds: float) -> GenerationMetrics:
    word_count = len(text.split())
    return GenerationMetrics(
        output_length=len(text),
        word_count=word_count,
        latency_seconds=latency_seconds,
        generation_speed_tokens_per_second=word_count / latency_seconds if latency_seconds > 0 else 0.0,
    )


def evaluate_generation(
    prediction: str,
    reference: str,
    latency_seconds: float,
    memory_usage_mb: float = 0.0,
    cpu_usage_percent: float = 0.0,
) -> GenerationMetrics:
    prediction_tokens = _tokens(prediction)
    reference_tokens = _tokens(reference)
    word_count = len(prediction_tokens)
    return GenerationMetrics(
        output_length=len(prediction),
        word_count=word_count,
        latency_seconds=latency_seconds,
        rouge_1=_rouge_1(prediction_tokens, reference_tokens),
        rouge_l=_rouge_l(prediction_tokens, reference_tokens),
        bleu=_bleu(prediction_tokens, reference_tokens),
        bert_score=_bert_score_fallback(prediction, reference),
        memory_usage_mb=memory_usage_mb,
        cpu_usage_percent=cpu_usage_percent,
        generation_speed_tokens_per_second=word_count / latency_seconds if latency_seconds > 0 else 0.0,
    )


def timed_evaluation(prediction: str, reference: str) -> GenerationMetrics:
    started_at = time.perf_counter()
    return evaluate_generation(prediction, reference, time.perf_counter() - started_at)


def _tokens(text: str) -> list[str]:
    return [token.strip(".,!?;:()[]{}\"'").lower() for token in text.split() if token.strip()]


def _rouge_1(prediction: list[str], reference: list[str]) -> float:
    if not prediction or not reference:
        return 0.0
    prediction_counts = Counter(prediction)
    reference_counts = Counter(reference)
    overlap = sum(min(prediction_counts[token], reference_counts[token]) for token in reference_counts)
    return overlap / len(reference)


def _rouge_l(prediction: list[str], reference: list[str]) -> float:
    if not prediction or not reference:
        return 0.0
    return _lcs_length(prediction, reference) / len(reference)


def _bleu(prediction: list[str], reference: list[str]) -> float:
    if not prediction or not reference:
        return 0.0
    unigram_precision = _rouge_1(prediction, reference)
    brevity_penalty = min(1.0, len(prediction) / len(reference))
    return unigram_precision * brevity_penalty


def _bert_score_fallback(prediction: str, reference: str) -> float:
    return SequenceMatcher(None, prediction.lower(), reference.lower()).ratio()


def _lcs_length(left: list[str], right: list[str]) -> int:
    previous = [0] * (len(right) + 1)
    for left_token in left:
        current = [0]
        for index, right_token in enumerate(right, start=1):
            if left_token == right_token:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current
    return previous[-1]
