# EduGen AI

Generate Complete Learning Materials using Open Source Generative AI.

EduGen AI is a university Generative AI final project built as a Python modular monolith. The first version uses Streamlit for the web app and keeps AI generation, data engineering, training, and evaluation as separate modules so each phase can be implemented and explained clearly.

## Current Status

This repository currently contains the full university project scaffold and working modules:

- Streamlit application shell
- Multi-page frontend
- Configuration layer
- Logging setup
- Validation utilities
- SQLite history storage
- AI prompt, inference, and dataset modules
- Data validation, splitting, metadata, and quality reporting
- Evaluation metrics, reports, experiments, and human scoring helpers
- Documentation structure
- Smoke checks and unit tests

Still optional/future:

- Model weight download and first real generation run
- Fine-tuning execution
- Presentation slides
- Evaluation dashboard UI

AI backend modules are present. Real local inference uses open-source Hugging Face models and needs the AI dependency group.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install full project extras used by this repository:

```bash
pip install -r requirements-ai.txt
pip install -r requirements-data.txt
pip install -r requirements-export.txt
pip install -r requirements-evaluation.txt
```

Training extras are only needed for actual fine-tuning:

```bash
pip install -r requirements-training.txt
```

## Start The App

```bash
PYTHONPATH=src streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Smoke Check

```bash
PYTHONPATH=src python scripts/smoke_check.py
```

## Run Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```

## Architecture

EduGen AI uses a modular monolith:

```text
app/                 Streamlit entrypoint
src/edugen/config/   application settings and logging
src/edugen/core/     validation, errors, business rules
src/edugen/ui/       Streamlit page rendering
src/edugen/ai/       prompts, inference, data, training hooks, evaluation
src/edugen/storage/  SQLite connection and repositories
src/edugen/exports/  Markdown, TXT, HTML, PDF export helpers
src/edugen/utils/    shared utility functions
datasets/            raw, processed, split, metadata, cache, downloads
outputs/             statistics and evaluation artifacts
docs/                planning and project documentation
tests/               runnable checks
```

See [PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md) before starting future work.

Useful docs:

- [Deployment](docs/DEPLOYMENT.md)
- [Demo Workflow](docs/DEMO_WORKFLOW.md)
- [Reproducibility](docs/REPRODUCIBILITY.md)
- [AI Pipeline](docs/AI_PIPELINE.md)
- [Data Pipeline](docs/DATA_PIPELINE.md)
- [Evaluation](docs/EVALUATION.md)
