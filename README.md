# EduGen AI

Generate Complete Learning Materials using Open Source Generative AI.

EduGen AI is a university Generative AI final project built as a Python modular monolith. The first version uses Streamlit for the web app and keeps AI generation, data engineering, training, and evaluation as separate modules so each phase can be implemented and explained clearly.

## Current Status

This repository currently contains the project foundation only.

- Streamlit application shell
- Basic page navigation
- Configuration layer
- Logging setup
- Validation utilities
- SQLite initialization skeleton
- Documentation structure
- Minimal tests

Not implemented yet:

- model download
- fine-tuning
- full dataset pipeline
- full evaluation framework

AI backend modules are present, but real local inference needs optional AI dependencies.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src streamlit run app/streamlit_app.py
```

## Run Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```

## Optional AI Dependencies

```bash
pip install -r requirements-ai.txt
```

Training dependencies are deferred:

```bash
pip install -r requirements-training.txt
```

## Architecture

EduGen AI uses a modular monolith:

```text
app/                 Streamlit entrypoint
src/edugen/config/   application settings and logging
src/edugen/core/     validation, errors, business rules
src/edugen/ui/       Streamlit page rendering
src/edugen/storage/  SQLite connection and repositories
src/edugen/utils/    shared utility functions
docs/                planning and project documentation
tests/               minimal runnable checks
```

See [PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md) before starting future work.
