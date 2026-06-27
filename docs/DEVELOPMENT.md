# Development Guide

Before starting work:

1. Read `docs/PROJECT_MEMORY.md`.
2. Scan the repository with `rg --files`.
3. Keep each prompt inside its phase boundary.
4. Run tests before committing.

Useful commands:

```bash
source .venv/bin/activate
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src python scripts/smoke_check.py
PYTHONPATH=src python -m compileall app src tests scripts
PYTHONPATH=src streamlit run app/streamlit_app.py
```

Data pipeline:

```bash
PYTHONPATH=src python -m edugen.ai.data.run_pipeline
```

Evaluation report:

```bash
PYTHONPATH=src python -m edugen.ai.evaluation.run_evaluation
```

Commit after each stable milestone:

```bash
git status
git add .
git commit -m "type: short milestone summary"
```
