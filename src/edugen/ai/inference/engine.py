import random
import time

from edugen.ai.config import GenerationConfig, ModelConfig
from edugen.ai.model_loader import ModelLoader
from edugen.ai.tokenizer import TokenizerManager
from edugen.core.exceptions import EduGenError


class InferenceManager:
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        tokenizer_manager: TokenizerManager | None = None,
        model_loader: ModelLoader | None = None,
    ) -> None:
        self.model_config = model_config or ModelConfig()
        self.tokenizer_manager = tokenizer_manager or TokenizerManager(self.model_config)
        self.model_loader = model_loader or ModelLoader(self.model_config)

    def generate(self, prompt: str, config: GenerationConfig | None = None) -> str:
        config = config or GenerationConfig()
        if config.seed is not None:
            random.seed(config.seed)

        started_at = time.perf_counter()
        tokenizer = self.tokenizer_manager.tokenizer
        model = self.model_loader.load()

        inputs = self._move_inputs_to_model_device(
            tokenizer(prompt, return_tensors="pt"),
            model,
        )
        try:
            outputs = model.generate(
                **inputs,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                repetition_penalty=config.repetition_penalty,
                do_sample=config.do_sample,
            )
        except RuntimeError as error:
            raise EduGenError(f"Generation failed: {error}") from error

        _ = time.perf_counter() - started_at
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _move_inputs_to_model_device(self, inputs, model):
        device = self._model_device(model)
        if device is None:
            return inputs
        return {
            name: value.to(device) if hasattr(value, "to") else value
            for name, value in inputs.items()
        }

    def _model_device(self, model):
        if hasattr(model, "device"):
            return model.device
        try:
            return next(model.parameters()).device
        except (AttributeError, StopIteration):
            return None
