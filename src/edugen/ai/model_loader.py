from edugen.ai.config import ModelConfig
from edugen.core.exceptions import EduGenError


class ModelLoader:
    _cache: dict[str, object] = {}

    def __init__(self, config: ModelConfig) -> None:
        self.config = config

    def load(self):
        if self.config.model_id not in self._cache:
            self._cache[self.config.model_id] = self._load_model()
        return self._cache[self.config.model_id]

    def validate(self) -> None:
        if not self.config.model_id:
            raise EduGenError("Model id is required.")

    def version_info(self) -> dict[str, str]:
        return {
            "model_id": self.config.model_id,
            "revision": self.config.revision,
            "license": self.config.license,
        }

    def _load_model(self):
        self.validate()
        try:
            from transformers import AutoModelForCausalLM
        except ImportError as error:
            raise EduGenError("Install transformers and torch to use model inference.") from error

        return AutoModelForCausalLM.from_pretrained(
            self.config.model_id,
            revision=self.config.revision,
            cache_dir=self.config.cache_dir,
            torch_dtype=self.config.torch_dtype,
            device_map=self.config.device,
            trust_remote_code=self.config.trust_remote_code,
        )
