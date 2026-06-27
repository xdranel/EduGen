import tempfile
import unittest
from pathlib import Path

from edugen.ai.evaluation.error_analysis import analyze_output
from edugen.ai.evaluation.experiments import ExperimentResult, ExperimentTracker
from edugen.ai.evaluation.human import HumanEvaluationForm
from edugen.ai.evaluation.metrics import evaluate_generation
from edugen.ai.evaluation.reports import EvaluationReportWriter


REFERENCE = "AI helps students learn with examples and quizzes."
PREDICTION = "AI helps students learn using examples and quizzes."


class EvaluationFrameworkTest(unittest.TestCase):
    def test_evaluate_generation_returns_quality_and_performance_metrics(self) -> None:
        metrics = evaluate_generation(PREDICTION, REFERENCE, latency_seconds=0.5)

        self.assertGreater(metrics.rouge_1, 0.7)
        self.assertGreater(metrics.bleu, 0.4)
        self.assertEqual(metrics.latency_seconds, 0.5)
        self.assertEqual(metrics.output_length, len(PREDICTION))

    def test_human_evaluation_form_computes_average(self) -> None:
        form = HumanEvaluationForm(
            correctness=5,
            coherence=4,
            readability=5,
            educational_value=4,
            completeness=3,
            grammar=5,
            relevance=4,
        )

        self.assertAlmostEqual(form.average_score(), 4.2857, places=3)

    def test_error_analysis_detects_repetition_and_missing_sections(self) -> None:
        analysis = analyze_output(
            "Learning Summary\nAI AI AI AI AI",
            required_sections=["Learning Summary", "References"],
        )

        self.assertIn("repetition", analysis.flags)
        self.assertIn("missing_sections", analysis.flags)

    def test_experiment_tracker_saves_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            tracker = ExperimentTracker(output_dir)
            tracker.save(
                ExperimentResult(
                    name="temperature-test",
                    model_id="local-model",
                    parameters={"temperature": 0.7},
                    metrics={"bleu": 0.5},
                )
            )

            saved = (output_dir / "experiments.jsonl").read_text(encoding="utf-8")

        self.assertIn("temperature-test", saved)
        self.assertIn("temperature", saved)

    def test_report_writer_outputs_markdown_html_and_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            writer = EvaluationReportWriter(output_dir)
            paths = writer.write_all(
                title="Evaluation",
                metrics={"bleu": 0.5, "rouge_1": 0.8},
                error_flags=["missing_sections"],
            )

            self.assertTrue(paths["markdown"].exists())
            self.assertTrue(paths["html"].exists())
            self.assertTrue(paths["csv"].exists())


if __name__ == "__main__":
    unittest.main()
