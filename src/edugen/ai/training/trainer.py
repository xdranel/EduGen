from edugen.ai.config import TrainingConfig
from edugen.core.exceptions import EduGenError


class TrainingManager:
    def __init__(self, config: TrainingConfig | None = None) -> None:
        self.config = config or TrainingConfig()

    def run(self) -> None:
        try:
            import peft  # noqa: F401
            import transformers  # noqa: F401
        except ImportError as error:
            raise EduGenError("Install transformers, peft, accelerate, and torch to train.") from error

        raise NotImplementedError("Training entrypoint is reserved for the training phase.")
