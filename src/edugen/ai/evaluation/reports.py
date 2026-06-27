import csv
from html import escape
from pathlib import Path


class EvaluationReportWriter:
    def __init__(self, output_dir: Path = Path("outputs/evaluation")) -> None:
        self.output_dir = output_dir

    def write_all(
        self,
        title: str,
        metrics: dict[str, float],
        error_flags: list[str],
    ) -> dict[str, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        paths = {
            "markdown": self.output_dir / "evaluation_report.md",
            "html": self.output_dir / "evaluation_report.html",
            "csv": self.output_dir / "evaluation_report.csv",
        }
        paths["markdown"].write_text(self._markdown(title, metrics, error_flags), encoding="utf-8")
        paths["html"].write_text(self._html(title, metrics, error_flags), encoding="utf-8")
        self._csv(paths["csv"], metrics, error_flags)
        try:
            paths["pdf"] = self._pdf(title, metrics, error_flags)
        except RuntimeError:
            pass
        return paths

    def _markdown(self, title: str, metrics: dict[str, float], error_flags: list[str]) -> str:
        lines = [f"# {title}", "", "## Metrics"]
        lines.extend(f"- {name}: {value}" for name, value in sorted(metrics.items()))
        lines.extend(["", "## Error Flags"])
        lines.extend(f"- {flag}" for flag in error_flags) if error_flags else lines.append("- None")
        return "\n".join(lines) + "\n"

    def _html(self, title: str, metrics: dict[str, float], error_flags: list[str]) -> str:
        metric_rows = "".join(
            f"<tr><td>{escape(name)}</td><td>{value}</td></tr>" for name, value in sorted(metrics.items())
        )
        flags = "".join(f"<li>{escape(flag)}</li>" for flag in error_flags) or "<li>None</li>"
        return (
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>{escape(title)}</title></head><body><h1>{escape(title)}</h1>"
            f"<table>{metric_rows}</table><h2>Error Flags</h2><ul>{flags}</ul></body></html>"
        )

    def _csv(self, path: Path, metrics: dict[str, float], error_flags: list[str]) -> None:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["metric", "value"])
            for name, value in sorted(metrics.items()):
                writer.writerow([name, value])
            writer.writerow(["error_flags", ";".join(error_flags)])

    def _pdf(self, title: str, metrics: dict[str, float], error_flags: list[str]) -> Path:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError as error:
            raise RuntimeError("Install reportlab for PDF evaluation reports.") from error

        path = self.output_dir / "evaluation_report.pdf"
        pdf = canvas.Canvas(str(path), pagesize=A4)
        _, height = A4
        y = height - 72
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(72, y, title)
        y -= 32
        pdf.setFont("Helvetica", 11)
        for name, value in sorted(metrics.items()):
            pdf.drawString(72, y, f"{name}: {value}")
            y -= 16
        y -= 12
        pdf.drawString(72, y, f"Error flags: {', '.join(error_flags) if error_flags else 'None'}")
        pdf.save()
        return path
