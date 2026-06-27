# Reproducibility Checklist

## Environment

- Python virtual environment created
- `requirements.txt` installed
- `requirements-ai.txt` installed for inference
- `requirements-data.txt` installed for data charts
- `requirements-export.txt` installed for PDF export
- `requirements-evaluation.txt` installed for richer evaluation metrics

## Commands

```bash
source .venv/bin/activate
PYTHONPATH=src python scripts/smoke_check.py
PYTHONPATH=src streamlit run app/streamlit_app.py
```

## Fixed Decisions

- Main language: Python
- App framework: Streamlit
- Architecture: modular monolith
- Default model: `Qwen/Qwen2.5-0.5B-Instruct`
- Storage: SQLite
- Dataset split: 80/10/10

## Artifacts

- Dataset metadata: `datasets/metadata/`
- Statistics: `outputs/statistics/`
- Evaluation reports: `outputs/evaluation/`
- Runtime logs: `logs/`

Generated artifacts are ignored by git.
