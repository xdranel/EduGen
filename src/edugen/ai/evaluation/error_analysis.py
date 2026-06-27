from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorAnalysis:
    flags: list[str]
    missing_sections: list[str]
    notes: list[str]


def analyze_output(
    text: str,
    required_sections: list[str] | None = None,
    min_words: int = 80,
    max_words: int = 3000,
) -> ErrorAnalysis:
    words = text.split()
    flags: list[str] = []
    notes: list[str] = []
    missing_sections = [
        section for section in (required_sections or []) if section.lower() not in text.lower()
    ]

    if _has_repetition(words):
        flags.append("repetition")
        notes.append("Repeated words or phrases detected.")
    if missing_sections:
        flags.append("missing_sections")
        notes.append("One or more required sections are missing.")
    if len(words) < min_words:
        flags.append("too_short")
        notes.append("Output is shorter than expected.")
    if len(words) > max_words:
        flags.append("too_long")
        notes.append("Output is longer than expected.")
    if any(marker in text.lower() for marker in ["i don't know", "as an ai language model", "citation needed"]):
        flags.append("hallucination_indicator")
        notes.append("Potential uncertainty or hallucination marker detected.")
    if text.strip().endswith(("...", ":", "-")):
        flags.append("incomplete_answer")
        notes.append("Output appears incomplete.")

    return ErrorAnalysis(flags, missing_sections, notes)


def _has_repetition(words: list[str]) -> bool:
    lowered = [word.lower().strip(".,!?;:") for word in words]
    for index in range(len(lowered) - 4):
        window = lowered[index : index + 5]
        if len(set(window)) <= 2:
            return True
    return False
