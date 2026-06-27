from collections import Counter

from edugen.ai.data.validator import ValidationProblem


def build_quality_report(problems: list[ValidationProblem]) -> str:
    counts = Counter(problem.kind for problem in problems)
    lines = [
        "# Dataset Quality Report",
        "",
        "## Problems",
    ]
    if not counts:
        lines.append("- No validation problems detected.")
    else:
        lines.extend(f"- {kind}: {count}" for kind, count in sorted(counts.items()))

    lines.extend(
        [
            "",
            "## Bias And Noise",
            "- Review source coverage before fine-tuning.",
            "- Filter non-educational and unsafe samples.",
            "",
            "## Coverage",
            "- Combine science QA, instruction data, assistant conversations, and textbook content.",
            "",
            "## Recommendations",
            "- Keep 80/10/10 split metadata for reproducibility.",
            "- Re-run validation after every dataset update.",
        ]
    )
    return "\n".join(lines) + "\n"
