# Development Guide

Before starting work:

1. Read `docs/PROJECT_MEMORY.md`.
2. Scan the repository with `rg --files`.
3. Keep each prompt inside its phase boundary.
4. Run tests before committing.

Useful commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src streamlit run app/streamlit_app.py
```
