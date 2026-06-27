from edugen.ai.config import ModelConfig
from edugen.core.exceptions import EduGenError


class TokenizerManager:
    def __init__(self, config: ModelConfig, tokenizer=None) -> None:
        self.config = config
        self._tokenizer = tokenizer

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = self.load()
        return self._tokenizer

    def load(self):
        try:
            from transformers import AutoTokenizer
        except ImportError as error:
            raise EduGenError("Install transformers to use the tokenizer.") from error

        return AutoTokenizer.from_pretrained(
            self.config.model_id,
            revision=self.config.revision,
            cache_dir=self.config.cache_dir,
            trust_remote_code=self.config.trust_remote_code,
        )

    def encode(self, text: str, max_length: int | None = None) -> list[int]:
        return self.tokenizer.encode(text, truncation=max_length is not None, max_length=max_length)

    def decode(self, token_ids: list[int]) -> str:
        return self.tokenizer.decode(token_ids, skip_special_tokens=True)

    def batch_encode(self, texts: list[str], max_length: int | None = None):
        return self.tokenizer(
            texts,
            padding=True,
            truncation=max_length is not None,
            max_length=max_length,
            return_tensors="pt",
        )
