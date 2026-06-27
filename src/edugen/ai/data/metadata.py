import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def dataclass_to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)
