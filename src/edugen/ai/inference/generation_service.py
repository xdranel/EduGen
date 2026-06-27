import time

from edugen.ai.config import GenerationConfig
from edugen.ai.inference.engine import InferenceManager
from edugen.ai.inference.output_formatter import GeneratedMaterial
from edugen.ai.inference.response_cleaner import ResponseCleaner
from edugen.ai.prompts.builder import PromptBuilder
from edugen.core.validation import validate_topic


class GenerationService:
    def __init__(
        self,
        prompt_builder: PromptBuilder | None = None,
        inference_engine: InferenceManager | None = None,
        response_cleaner: ResponseCleaner | None = None,
    ) -> None:
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.inference_engine = inference_engine or InferenceManager()
        self.response_cleaner = response_cleaner or ResponseCleaner()

    def generate_material(
        self,
        topic: str,
        difficulty: str = "Beginner",
        language: str = "English",
        quiz_count: int = 5,
        config: GenerationConfig | None = None,
    ) -> GeneratedMaterial:
        topic = validate_topic(topic)
        prompt = self.prompt_builder.educational_material(
            topic=topic,
            difficulty=difficulty,
            language=language,
            quiz_count=quiz_count,
        )

        started_at = time.perf_counter()
        raw = self.inference_engine.generate(prompt, config or GenerationConfig())
        content = self.response_cleaner.clean(raw)

        return GeneratedMaterial(
            topic=topic,
            content=content,
            prompt=prompt,
            elapsed_seconds=time.perf_counter() - started_at,
        )
