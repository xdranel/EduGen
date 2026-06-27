# EduGen AI Project Memory

This file is the working memory for EduGen AI. Before starting any future task, reread this file and rescan the repository so new prompts can be filtered against existing decisions, skipped work, and current progress.

## Current State

- Project name: EduGen AI
- Tagline: Generate Complete Learning Materials using Open Source Generative AI
- Repository status: Prompt 5 evaluation framework implemented
- Installed by user: `streamlit`
- Current files: project foundation, Streamlit frontend, AI backend modules, data pipeline modules, evaluation modules, tests, docs, config, storage skeleton
- Current architecture decision: Python modular monolith
- Main app framework: Streamlit
- AI stack direction: optional PyTorch, Hugging Face Transformers, PEFT, LoRA or QLoRA, Datasets, Accelerate
- Storage direction: SQLite when history/settings are implemented

## Core Requirement Summary

EduGen AI must generate new educational learning materials from a single topic entered by the user.

Required generated sections:

- Learning Summary
- Detailed Explanation
- Key Concepts
- Real-life Analogy
- Examples
- Important Notes
- Flashcards
- Multiple Choice Quiz
- Essay Questions
- Answer Key
- Mini Project
- Learning Roadmap
- References

University constraints:

- Do not use OpenAI API
- Do not use Gemini API
- Do not use Claude API
- Do not use closed-source LLM providers
- Use open-source models
- Keep the AI pipeline explainable
- Make training, fine-tuning, and inference reproducible
- Keep the architecture understandable for students

## Architecture Decision

Use a Python modular monolith.

Reason:

- The whole AI stack is Python-native.
- Streamlit is enough for the first polished UI.
- Microservices add unnecessary deployment and debugging cost.
- Spring Boot plus Python would mostly wrap Python inference and slow development.

Deferred:

- FastAPI backend
- React frontend
- Microservices
- Spring Boot service layer
- PostgreSQL
- Vector database

Add those only when the project has real API, scale, or integration needs.

## Planned Folder Direction

Initial target structure:

```text
edugen-ai/
├── app/
│   └── streamlit_app.py
├── src/
│   └── edugen/
│       ├── config/
│       ├── ui/
│       ├── core/
│       ├── ai/
│       │   ├── prompts/
│       │   ├── inference/
│       │   ├── training/
│       │   └── evaluation/
│       ├── data/
│       ├── storage/
│       ├── exports/
│       └── utils/
├── datasets/
├── models/
├── notebooks/
├── scripts/
├── tests/
├── docs/
├── outputs/
├── requirements.txt
├── README.md
└── .env.example
```

Keep this structure minimal at first. Do not create empty folders unless they are needed by the next task.

## Working Rules For Future Prompts

Before doing any task:

1. Reread this file.
2. Rescan the repository with `rg --files` or equivalent.
3. Check whether the request is already decided, already implemented, or deferred.
4. Extract only actionable requirements from long prompts.
5. Update this file after meaningful decisions, blockers, or completed milestones.

Prompt handling rule:

- Do not implement future-phase work early.
- Prompt 2 creates foundation only.
- Prompt 3 creates AI backend only.
- Prompt 4 creates frontend and integrates AI backend.
- Prompt 4.5 creates data engineering pipeline.
- Prompt 5 creates evaluation framework.
- If a prompt asks for something already implemented, inspect existing code and extend it instead of recreating it.

## Prompt Sequence Map

| Prompt | Purpose | Implement Now? | Notes |
| --- | --- | --- | --- |
| Prompt 1 | Architecture document only | Done conceptually, document still needed if requested | No code. Covers model, dataset, pipeline, architecture, UI, DB, training, evaluation, risks, roadmap. |
| Prompt 2 | Repository foundation | Next implementation phase | Create executable structure, docs, config, logging, exceptions, basic Streamlit pages, tests. No AI generation, training, or inference. |
| Prompt 3 | AI backend pipeline | Later | Model/tokenizer loading, prompts, generation service, dataset manager basics, preprocessing, optional LoRA/QLoRA training, evaluation metrics hooks. No UI redesign. |
| Prompt 4 | Streamlit frontend | Later | Multi-page UI, generation form, progress display, history, downloads, settings, AI backend integration. |
| Prompt 4.5 | Data engineering pipeline | Later | Dataset recommendation, downloader, validation, cleaning, splitting, statistics, visualizations, metadata, reports. |
| Prompt 5 | Evaluation framework | Later | ROUGE, BLEU, BERTScore, latency, memory/CPU usage, human evaluation, experiments, reports. |

## Prompt 2 Scope Guard

When implementing Prompt 2, include:

- Minimal GitHub-ready repository files
- `README.md`
- `LICENSE`
- `.gitignore`
- `requirements.txt`
- `environment.yml`
- `pyproject.toml`
- `Dockerfile`
- `docker-compose.yml`
- config modules
- logging setup
- custom exceptions
- validation utilities
- basic reusable utilities
- SQLite connection/repository skeleton only if history/settings foundation needs it
- Streamlit app shell
- placeholder pages: Home, Generate, History, Downloads, Settings, About
- example tests
- documentation files

When implementing Prompt 2, skip:

- real AI generation
- model downloads
- training
- inference
- dataset downloads
- heavy AI dependencies
- polished final SaaS UI behavior

## Later Phase Notes

Prompt 3 AI backend should keep model choice configurable. Do not hardcode one model throughout the code.

Prompt 4 UI should not become one large `app.py`; keep Streamlit page code separate from services and business logic.

Prompt 4.5 data pipeline may be more logically implemented before Prompt 3 training work if real fine-tuning is required. If the user follows file order exactly, keep Prompt 3 training optional and make the app work without training.

Prompt 5 evaluation should save artifacts under `outputs/evaluation/`.

Prompt 3 implementation note: AI modules are importable without heavy dependencies. Real local model inference requires `pip install -r requirements-ai.txt`. Training requires `pip install -r requirements-training.txt`.

Prompt 4 implementation note: PDF export is optional and requires `pip install -r requirements-export.txt`. Markdown, TXT, and HTML exports use the standard library.

Prompt 4.5 implementation note: data-pipeline PNG charts require `pip install -r requirements-data.txt`; without matplotlib the pipeline still writes CSV statistics.

Prompt 5 implementation note: evaluation works with stdlib fallbacks. Optional richer ROUGE/BLEU/BERTScore/resource tooling is listed in `requirements-evaluation.txt`.

## Progress Log

| Date | Progress |
| --- | --- |
| 2026-06-27 | Chose Python modular monolith with Streamlit as the application framework. |
| 2026-06-27 | Created project memory document for tracking decisions, progress, blockers, and future prompt filtering. |
| 2026-06-27 | Read Prompt 1, Prompt 2, Prompt 3, Prompt 4, Prompt 4.5, and Prompt 5 from `/home/xdranel/Code/Prompt`. |
| 2026-06-27 | User initialized project preparation and generated `requirements.txt` after installing Streamlit. |
| 2026-06-27 | Implemented Prompt 2 foundation: repository metadata, Streamlit shell, config, logging, validation, SQLite skeleton, docs, and tests. |
| 2026-06-27 | Verified foundation with unit tests, compile check, import check, and short Streamlit launch check. |
| 2026-06-27 | Implemented Prompt 3 AI backend: model config/registry, prompt builder, preprocessing, dataset manager/downloader, tokenizer wrapper, model loader, inference service, lightweight metrics, training hooks, docs, and tests. |
| 2026-06-27 | Verified AI backend with 11 unit tests, compile check, import check, and short Streamlit launch check. |
| 2026-06-27 | Implemented Prompt 4 frontend: richer Streamlit navigation, generate form, AI backend integration, progress/status UI, output sections, history, downloads, settings, and about page. |
| 2026-06-27 | Verified frontend with 14 unit tests, compile check, import check, and short Streamlit launch check. |
| 2026-06-27 | Implemented Prompt 4.5 data pipeline: dataset recommendations, downloader extraction/checksum, validation, splitting, statistics, metadata, quality reports, docs, and tests. |
| 2026-06-27 | Verified data pipeline with 19 unit tests, compile check, temporary pipeline run, and short Streamlit launch check from `.venv`. |
| 2026-06-27 | Implemented Prompt 5 evaluation framework: ROUGE/BLEU/BERTScore fallback metrics, latency/speed/resource fields, human scoring, experiments, visualizations, error analysis, reports, docs, and tests. |
| 2026-06-27 | Verified evaluation framework with 24 unit tests, compile check, sample report generation, and short Streamlit launch check from `.venv`. |

## Problems And Blockers

| Date | Problem | Status | Future Fix |
| --- | --- | --- | --- |
| 2026-06-27 | No actual app structure exists yet. | Closed | Prompt 2 foundation created. |
| 2026-06-27 | Model choice not finalized. | Closed | Default model set to `Qwen/Qwen2.5-0.5B-Instruct`, configurable through `ModelConfig`. |
| 2026-06-27 | Dataset choice not finalized. | Closed | Recommended SciQ, Dolly 15k, OpenAssistant OASST1, and OpenStax source material. |
| 2026-06-27 | `requirements.txt` contains Streamlit and transitive dependencies only. | Closed | Added optional `requirements-ai.txt` and `requirements-training.txt`; base app remains lightweight. |
| 2026-06-27 | PDF export dependency not installed by default. | Closed | User installed `requirements-export.txt` in `.venv`; verified `reportlab` import. |
| 2026-06-27 | Current assistant shell cannot import `torch` or `transformers`. | Closed | Verified `.venv` can import `torch` and `transformers`; use `.venv/bin/python` or activate `.venv`. |
| 2026-06-27 | Matplotlib is not installed in `.venv`. | Closed | User installed `requirements-data.txt`; verified matplotlib import. |
| 2026-06-27 | Full external evaluation metrics not installed by default. | Open | Run `pip install -r requirements-evaluation.txt` only if real `bert-score`, `rouge-score`, `sacrebleu`, and `psutil` are required. |

## Decision Log

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-06-27 | Use Python as the main language. | Best support for open-source LLM training and inference. |
| 2026-06-27 | Use Streamlit as the first app framework. | Fastest path to a usable AI product UI for a university project. |
| 2026-06-27 | Use modular monolith architecture. | Professional enough without microservice overhead. |
| 2026-06-27 | Avoid Spring Boot for the first version. | Adds a second backend stack without improving the AI core. |
| 2026-06-27 | Keep dependencies phase-based. | Heavy AI packages are version-sensitive and should not be installed before model/hardware choices are clear. |
| 2026-06-27 | Use explicit unittest discovery. | `python -m unittest` ran zero tests in this environment; use `python -m unittest discover -s tests -p 'test_*.py'`. |
| 2026-06-27 | Default to `Qwen/Qwen2.5-0.5B-Instruct`. | Small, instruction-tuned, Hugging Face Transformers-compatible, Apache-2.0, and practical for student hardware. |

## Deferred Ideas

- FastAPI API layer
- React frontend
- User authentication
- LMS integration
- RAG with vector database
- Voice generation
- Image generation
- Mobile app
- Deployment automation beyond the first local/demo version
- Fine-tuning
- Real model inference run on downloaded weights
- Full dataset download/preprocessing
- Full evaluation dashboard UI

## Next Likely Work

Next phase is Prompt #6: deployment, final documentation, demo polish, or project packaging.

Prompt #6 should implement:

- deployment instructions
- final README cleanup
- demo workflow
- reproducibility checklist
- presentation/report assets
- optional evaluation dashboard UI
- final dependency lock and sanity test
