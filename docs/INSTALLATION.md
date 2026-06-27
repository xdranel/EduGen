# Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src streamlit run app/streamlit_app.py
```

AI dependencies are intentionally deferred until the model and hardware target are selected.

Optional PDF export:

```bash
pip install -r requirements-export.txt
```

Optional data-pipeline charts and Hugging Face dataset loading:

```bash
pip install -r requirements-data.txt
```

Optional richer evaluation metrics:

```bash
pip install -r requirements-evaluation.txt
```
