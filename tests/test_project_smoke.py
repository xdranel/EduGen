import unittest

from edugen.ai.config import ModelConfig
from edugen.ai.data.recommendations import recommended_datasets
from edugen.ai.evaluation.metrics import evaluate_generation
from edugen.config.settings import AppSettings


class ProjectSmokeTest(unittest.TestCase):
    def test_project_identity_and_core_modules_are_available(self) -> None:
        self.assertEqual(AppSettings().app_name, "EduGen AI")
        self.assertEqual(ModelConfig().model_id, "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertGreaterEqual(len(recommended_datasets()), 4)

    def test_evaluation_metric_smoke(self) -> None:
        metrics = evaluate_generation("AI helps students learn.", "AI helps learners study.", 0.1)

        self.assertGreaterEqual(metrics.rouge_1, 0.0)
        self.assertGreater(metrics.generation_speed_tokens_per_second, 0.0)


if __name__ == "__main__":
    unittest.main()
