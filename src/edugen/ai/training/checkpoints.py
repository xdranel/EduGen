from pathlib import Path


class CheckpointManager:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def latest(self) -> Path | None:
        if not self.output_dir.exists():
            return None
        checkpoints = sorted(self.output_dir.glob("checkpoint-*"))
        return checkpoints[-1] if checkpoints else None
