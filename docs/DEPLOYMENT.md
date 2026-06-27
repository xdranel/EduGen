# Deployment

EduGen AI is a Streamlit modular monolith. The simplest demo deployment is local or Docker-based.

## Local Demo

```bash
source .venv/bin/activate
PYTHONPATH=src streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Docker Demo

```bash
docker compose up --build
```

The app listens on port `8501`.

## Environment

Use `.env.example` as the starting point:

```text
EDUGEN_ENV=development
EDUGEN_LOG_LEVEL=INFO
EDUGEN_DATABASE_PATH=database/edugen.db
```

## Notes

- First local model generation may download model weights.
- Keep `models/`, `datasets/`, `outputs/`, `database/`, and `logs/` out of git.
- Use CPU for demo safety unless CUDA is already working.
