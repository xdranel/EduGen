# Folder Structure

| Path | Purpose |
| --- | --- |
| `app/` | Streamlit entrypoint. |
| `src/edugen/config/` | Settings, constants, and logging. |
| `src/edugen/core/` | Validation, exceptions, and future business rules. |
| `src/edugen/ai/` | Open-source AI pipeline, data pipeline, training hooks, and evaluation framework. |
| `src/edugen/ui/` | Streamlit page rendering. |
| `src/edugen/storage/` | SQLite connection and repositories. |
| `src/edugen/exports/` | Markdown, TXT, HTML, and optional PDF export helpers. |
| `src/edugen/utils/` | Small reusable helpers. |
| `scripts/` | Local maintenance and smoke-check scripts. |
| `docs/` | Architecture notes and project memory. |
| `tests/` | Runnable checks for foundation, AI pipeline, frontend support, data pipeline, evaluation, and smoke behavior. |
| `database/` | Local SQLite files, ignored by git. |
| `logs/` | Runtime log files, ignored by git. |
| `outputs/` | Generated exports and reports, ignored by git. |
| `outputs/statistics/` | Chart and CSV outputs from data analysis. |
| `outputs/evaluation/` | Evaluation reports, experiment logs, and metric charts. |
| `models/` | Local model files, ignored by git. |
| `datasets/` | Raw and processed datasets, ignored by git. |
| `datasets/raw/` | Source files before cleaning. |
| `datasets/processed/` | Unified cleaned JSONL dataset. |
| `datasets/train/` | Training split. |
| `datasets/validation/` | Validation split. |
| `datasets/test/` | Test split. |
| `datasets/metadata/` | Dataset metadata, split metadata, validation logs, and quality reports. |
| `datasets/cache/` | Reusable preprocessing cache. |
| `datasets/statistics/` | Dataset-local statistics artifacts. |
| `datasets/downloads/` | Downloaded archives and source files. |
