from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    python = sys.executable
    run([python, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
    run([python, "-m", "compileall", "app", "src", "tests"])
    run([python, "-m", "edugen.ai.evaluation.run_evaluation"])
    print("SMOKE CHECK COMPLETE")


if __name__ == "__main__":
    main()
