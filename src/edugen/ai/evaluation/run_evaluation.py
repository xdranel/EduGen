from edugen.ai.evaluation.error_analysis import analyze_output
from edugen.ai.evaluation.metrics import evaluate_generation
from edugen.ai.evaluation.reports import EvaluationReportWriter


def main() -> None:
    reference = "EduGen AI creates structured educational materials from a topic."
    prediction = "EduGen AI creates educational materials from one topic."
    metrics = evaluate_generation(prediction, reference, latency_seconds=0.0)
    analysis = analyze_output(
        prediction,
        required_sections=["Learning Summary", "References"],
        min_words=1,
    )
    EvaluationReportWriter().write_all(
        "EduGen AI Evaluation Report",
        metrics.__dict__,
        analysis.flags,
    )
    print("Evaluation report written to outputs/evaluation/")


if __name__ == "__main__":
    main()
