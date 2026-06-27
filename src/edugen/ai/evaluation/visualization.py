import csv
import os
from pathlib import Path


def write_metric_series(name: str, values: list[float], output_dir: Path = Path("outputs/evaluation")) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{name}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["step", "value"])
        for index, value in enumerate(values):
            writer.writerow([index, value])

    _try_plot(name, values, output_dir / f"{name}.png")
    return csv_path


def _try_plot(name: str, values: list[float], path: Path) -> None:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    plt.figure()
    plt.plot(values)
    plt.title(name.replace("_", " ").title())
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
