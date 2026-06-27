import csv
import os
from pathlib import Path


def write_length_distribution(lengths: list[int], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "length_distribution.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["sample_index", "token_count"])
        for index, length in enumerate(lengths):
            writer.writerow([index, length])

    try:
        os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    plt.figure()
    plt.hist(lengths, bins=min(20, max(1, len(lengths))))
    plt.title("Dataset Length Distribution")
    plt.xlabel("Token count")
    plt.ylabel("Samples")
    plt.tight_layout()
    plt.savefig(output_dir / "length_distribution.png")
    plt.close()
