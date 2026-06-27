import json
import tempfile
import unittest
from pathlib import Path

from edugen.ai.config import GenerationConfig, ModelConfig
from edugen.ai.data.dataset_downloader import DatasetDownloader
from edugen.ai.data.dataset_manager import DatasetManager
from edugen.ai.evaluation.metrics import basic_generation_metrics
from edugen.ai.inference.engine import InferenceManager
from edugen.ai.inference.generation_service import GenerationService
from edugen.ai.preprocessing.cleaner import TextPreprocessor
from edugen.ai.prompts.builder import PromptBuilder
from edugen.ai.tokenizer import TokenizerManager


class FakeInferenceEngine:
    def generate(self, prompt: str, config: GenerationConfig) -> str:
        return f"Generated from: {prompt[:32]}"


class FakeTokenizer:
    def encode(self, text: str, truncation: bool = False, max_length: int | None = None) -> list[int]:
        tokens = [len(word) for word in text.split()]
        return tokens[:max_length] if truncation and max_length else tokens

    def decode(self, token_ids: list[int], skip_special_tokens: bool = True) -> str:
        return " ".join(str(token_id) for token_id in token_ids)

    def __call__(self, texts: list[str], **kwargs: object) -> dict[str, list[list[int]]]:
        return {"input_ids": [self.encode(text) for text in texts]}


class FakeTensor:
    def __init__(self) -> None:
        self.moved_to = None

    def to(self, device: str) -> "FakeTensor":
        self.moved_to = device
        return self


class FakeBatch(dict):
    def __init__(self) -> None:
        super().__init__(input_ids=FakeTensor())


class FakeTorchTokenizer:
    def __call__(self, prompt: str, return_tensors: str) -> FakeBatch:
        return FakeBatch()

    def decode(self, output: object, skip_special_tokens: bool = True) -> str:
        return "decoded"


class FakeCudaModel:
    device = "cuda:0"

    def __init__(self) -> None:
        self.received_inputs = None

    def generate(self, **inputs: object) -> list[str]:
        self.received_inputs = inputs
        return ["tokens"]


class FakeModelLoader:
    def __init__(self, model: FakeCudaModel) -> None:
        self.model = model

    def load(self) -> FakeCudaModel:
        return self.model


class FakeTokenizerManager:
    tokenizer = FakeTorchTokenizer()


class AiPipelineTest(unittest.TestCase):
    def test_model_config_defaults_to_recommended_open_model(self) -> None:
        config = ModelConfig()

        self.assertEqual(config.model_id, "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(config.license, "apache-2.0")

    def test_preprocessor_cleans_and_deduplicates_text(self) -> None:
        preprocessor = TextPreprocessor()

        cleaned = preprocessor.clean_many(["  Learn   AI\n", "Learn AI", "", "Use <b>models</b>"])

        self.assertEqual(cleaned, ["Learn AI", "Use models"])

    def test_prompt_builder_includes_required_sections(self) -> None:
        prompt = PromptBuilder().educational_material(
            topic="photosynthesis",
            difficulty="Beginner",
            language="English",
            quiz_count=3,
        )

        self.assertIn("Learning Summary", prompt)
        self.assertIn("Flashcards", prompt)
        self.assertIn("Multiple Choice Quiz", prompt)
        self.assertIn("photosynthesis", prompt)

    def test_dataset_manager_loads_json_csv_and_txt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "samples.json").write_text(
                json.dumps([{"instruction": "Explain AI", "output": "AI is..."}]),
                encoding="utf-8",
            )
            (root / "samples.csv").write_text(
                "instruction,output\nExplain ML,ML is...\n",
                encoding="utf-8",
            )
            (root / "samples.txt").write_text("Explain data science\n", encoding="utf-8")

            records = DatasetManager(root).load_all()

        instructions = {record.instruction for record in records}

        self.assertEqual(len(records), 3)
        self.assertIn("Explain AI", instructions)
        self.assertIn("Explain ML", instructions)
        self.assertIn("Explain data science", instructions)

    def test_generation_service_uses_prompt_and_engine(self) -> None:
        service = GenerationService(
            prompt_builder=PromptBuilder(),
            inference_engine=FakeInferenceEngine(),
        )

        result = service.generate_material("machine learning")

        self.assertEqual(result.topic, "machine learning")
        self.assertIn("Generated from:", result.content)

    def test_tokenizer_manager_wraps_encoding_decoding(self) -> None:
        manager = TokenizerManager(ModelConfig(), tokenizer=FakeTokenizer())

        self.assertEqual(manager.encode("open source model", max_length=2), [4, 6])
        self.assertEqual(manager.decode([4, 6]), "4 6")

    def test_basic_generation_metrics_counts_output(self) -> None:
        metrics = basic_generation_metrics("AI helps students learn", latency_seconds=0.5)

        self.assertEqual(metrics.output_length, 23)
        self.assertEqual(metrics.word_count, 4)
        self.assertEqual(metrics.latency_seconds, 0.5)

    def test_inference_manager_moves_inputs_to_model_device(self) -> None:
        model = FakeCudaModel()
        manager = InferenceManager(
            tokenizer_manager=FakeTokenizerManager(),
            model_loader=FakeModelLoader(model),
        )

        result = manager.generate("Explain AI", GenerationConfig(max_new_tokens=4))

        self.assertEqual(result, "decoded")
        self.assertEqual(model.received_inputs["input_ids"].moved_to, "cuda:0")

    def test_dataset_downloader_copies_file_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.txt"
            target_dir = root / "downloads"
            source.write_text("dataset sample", encoding="utf-8")

            downloaded = DatasetDownloader(target_dir).download(source.as_uri())

        self.assertEqual(downloaded.name, "source.txt")


if __name__ == "__main__":
    unittest.main()
