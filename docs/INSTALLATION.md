# Installation

## Base App

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Full Demo Install

Install the dependency groups used by the current project:

```bash
pip install -r requirements-ai.txt
pip install -r requirements-data.txt
pip install -r requirements-export.txt
pip install -r requirements-evaluation.txt
```

Install training dependencies only when running fine-tuning:

```bash
pip install -r requirements-training.txt
```

## Start

```bash
PYTHONPATH=src streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`.

## Verify

```bash
PYTHONPATH=src python scripts/smoke_check.py
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```

## Dependency Groups

| File | Purpose |
| --- | --- |
| `requirements.txt` | Streamlit app and base dependencies. |
| `requirements-ai.txt` | Local open-source model inference. |
| `requirements-data.txt` | Data pipeline, Hugging Face datasets, matplotlib charts. |
| `requirements-export.txt` | PDF export through ReportLab. |
| `requirements-evaluation.txt` | BERTScore, ROUGE, BLEU, resource metrics, charting. |
| `requirements-training.txt` | Fine-tuning support with PEFT/datasets/matplotlib. |

## Docker

```bash
docker compose up --build
```
