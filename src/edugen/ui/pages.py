import streamlit as st

from edugen.ai.config import GenerationConfig, ModelConfig
from edugen.ai.inference.generation_service import GenerationService
from edugen.ai.inference.output_formatter import GeneratedMaterial
from edugen.ai.model_registry import SUPPORTED_MODELS
from edugen.config.settings import AppSettings
from edugen.core.exceptions import format_error
from edugen.exports.document_exporter import DocumentExporter
from edugen.storage.history_repository import HistoryRecord, HistoryRepository
from edugen.ui.content_parser import ContentSection, split_sections
from edugen.utils.date_utils import utc_now_iso


def render_page(page: str, settings: AppSettings) -> None:
    pages = {
        "Home": _home_page,
        "Generate Learning Material": _generate_page,
        "History": _history_page,
        "Downloads": _downloads_page,
        "Settings": _settings_page,
        "About": _about_page,
    }
    pages.get(page, _home_page)(settings)


def _home_page(settings: AppSettings) -> None:
    st.title(settings.app_name)
    st.subheader(settings.tagline)
    st.write("Create summaries, explanations, flashcards, quizzes, mini projects, and roadmaps from one topic.")

    col1, col2, col3 = st.columns(3)
    col1.metric("AI core", "Open source")
    col2.metric("Architecture", "Modular")
    col3.metric("Storage", "SQLite")

    st.markdown("### What it generates")
    c1, c2, c3, c4 = st.columns(4)
    c1.info("Summaries")
    c2.info("Flashcards")
    c3.info("Quizzes")
    c4.info("Roadmaps")

    st.markdown("### Architecture")
    st.write("Python modular monolith with Streamlit, SQLite, and a future local LLM pipeline.")
    st.markdown("### Supported models")
    for model in SUPPORTED_MODELS.values():
        st.write(f"**{model.model_id}** - {model.size}, {model.license}")


def _generate_page(settings: AppSettings) -> None:
    st.title("Generate Learning Material")
    st.caption("Uses the local open-source AI backend. First run may download the configured model.")

    with st.form("generate_form"):
        topic = st.text_input("Topic")
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        language = st.selectbox("Language", ["English", "Indonesian"], index=0)
        output_length = st.selectbox("Output Length", ["Short", "Medium", "Long"], index=1)
        quiz_count = st.number_input("Quiz Count", min_value=1, max_value=20, value=5)

        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            top_p = st.slider("Top-P", 0.1, 1.0, 0.9, 0.05)
            top_k = st.number_input("Top-K", min_value=1, max_value=200, value=50)
            max_new_tokens = st.number_input("Maximum Tokens", min_value=128, max_value=4096, value=_tokens_for_length(output_length))
            seed = st.number_input("Seed", min_value=0, max_value=999999, value=42)

        left, right = st.columns([1, 1])
        submitted = left.form_submit_button("Generate")
        reset = right.form_submit_button("Reset")

    if reset:
        st.session_state.pop("last_result", None)
        st.rerun()

    if submitted:
        try:
            config = GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=int(top_k),
                max_new_tokens=int(max_new_tokens),
                seed=int(seed),
            )
            result = _run_generation(topic, difficulty, language, int(quiz_count), config)
        except ValueError as error:
            st.error(format_error(error))
        except Exception as error:
            st.error(format_error(error))
            st.info("If this is a missing dependency or model download issue, install `requirements-ai.txt` and retry.")
        else:
            st.session_state["last_result"] = result
            _save_history(settings, result, difficulty, language)

    if "last_result" in st.session_state:
        _render_generated_material(st.session_state["last_result"])


def _history_page(settings: AppSettings) -> None:
    st.title("History")
    repository = HistoryRepository(settings.database_path)
    query = st.text_input("Search history")
    records = repository.search(query) if query else repository.list()

    if not records:
        st.info("No generated materials found yet.")
        return

    exporter = DocumentExporter()
    for record in records:
        with st.expander(f"{record.topic} - {record.created_at}", expanded=False):
            st.caption(f"{record.difficulty} | {record.language}")
            st.markdown(record.content[:2000])
            col1, col2, col3 = st.columns(3)
            col1.download_button("Download Markdown", exporter.to_markdown(record.topic, record.content), file_name=f"{record.topic}.md")
            if col2.button("Reuse", key=f"reuse-{record.id}"):
                st.session_state["last_result"] = GeneratedMaterial(record.topic, record.content, "", 0.0)
                st.success("Loaded into current result.")
            if col3.button("Delete", key=f"delete-{record.id}"):
                repository.delete(record.id)
                st.rerun()


def _downloads_page(settings: AppSettings) -> None:
    st.title("Downloads")
    result = st.session_state.get("last_result")
    if result is None:
        st.info("Generate or reuse a material first.")
        return

    exporter = DocumentExporter()
    topic = result.topic
    content = result.content

    st.write(f"Current material: **{topic}**")
    col1, col2, col3, col4 = st.columns(4)
    col1.download_button("Markdown", exporter.to_markdown(topic, content), file_name=f"{topic}.md")
    col2.download_button("TXT", exporter.to_text(topic, content), file_name=f"{topic}.txt")
    col3.download_button("HTML", exporter.to_html(topic, content), file_name=f"{topic}.html", mime="text/html")
    try:
        pdf = exporter.to_pdf(topic, content)
    except RuntimeError:
        col4.info("Install `reportlab` for PDF.")
    else:
        col4.download_button("PDF", pdf, file_name=f"{topic}.pdf", mime="application/pdf")


def _settings_page(settings: AppSettings) -> None:
    st.title("Settings")
    model_ids = list(SUPPORTED_MODELS)
    selected_model = st.selectbox("Model", model_ids, index=0)
    st.session_state["model_id"] = selected_model
    st.session_state["theme"] = st.selectbox("Theme", ["Light", "Dark"])
    st.session_state["language"] = st.selectbox("Default language", ["English", "Indonesian"])
    st.selectbox("Default export format", ["Markdown", "PDF", "TXT", "HTML"])
    st.info("Settings are kept in session for now. Persistent settings can be added when user accounts exist.")


def _about_page(settings: AppSettings) -> None:
    st.title("About")
    st.write(settings.tagline)
    st.write("EduGen AI is a university Generative AI final project using local open-source models.")
    st.write("Technology: Python, Streamlit, SQLite, Hugging Face Transformers, PyTorch.")
    st.write("Architecture: modular monolith with separated UI, AI backend, storage, exports, and utilities.")
    st.write(f"Version: {settings.version}")
    st.write("License: MIT")
    st.write("Authors: to be completed")


def _run_generation(
    topic: str,
    difficulty: str,
    language: str,
    quiz_count: int,
    config: GenerationConfig,
) -> GeneratedMaterial:
    progress = st.progress(0)
    status = st.empty()
    stages = ["Validating input", "Building prompt", "Loading model", "Generating material", "Cleaning output"]

    for index, stage in enumerate(stages[:-1], start=1):
        status.write(stage)
        progress.progress(index / len(stages))

    service = _generation_service(st.session_state.get("model_id", "Qwen/Qwen2.5-0.5B-Instruct"))
    result = service.generate_material(topic, difficulty, language, quiz_count, config)
    status.write(stages[-1])
    progress.progress(1.0)
    st.success(f"Generated in {result.elapsed_seconds:.2f}s")
    return result


@st.cache_resource(show_spinner=False)
def _generation_service(model_id: str) -> GenerationService:
    from edugen.ai.inference.engine import InferenceManager

    model_config = ModelConfig(model_id=model_id)
    return GenerationService(inference_engine=InferenceManager(model_config=model_config))


def _save_history(settings: AppSettings, result: GeneratedMaterial, difficulty: str, language: str) -> None:
    HistoryRepository(settings.database_path).add(
        HistoryRecord(
            topic=result.topic,
            difficulty=difficulty,
            language=language,
            content=result.content,
            created_at=utc_now_iso(),
        )
    )


def _render_generated_material(result: GeneratedMaterial) -> None:
    st.markdown("## Generated Material")
    st.caption(f"Topic: {result.topic} | Elapsed: {result.elapsed_seconds:.2f}s")

    sections = split_sections(result.content)
    if not sections:
        st.markdown(result.content)
        return

    for section in sections:
        _render_section(section)


def _render_section(section: ContentSection) -> None:
    with st.expander(section.title, expanded=section.title in {"Learning Summary", "Detailed Explanation"}):
        if section.title.lower().startswith("flashcard"):
            _render_flashcards(section.body)
        elif "quiz" in section.title.lower():
            _render_quiz(section.body)
        elif "mini project" in section.title.lower():
            st.markdown(section.body)
        else:
            st.markdown(section.body)

        st.text_area("Copy section text", section.body, height=120, key=f"copy-{section.title}")
        col1, col2 = st.columns(2)
        if col1.button("Regenerate Section", key=f"regen-{section.title}"):
            st.info("Use Generate to refresh the full material. Single-section regeneration will be added after section-level prompts are tuned.")
        col2.download_button(
            "Download Section",
            section.body,
            file_name=f"{section.title.lower().replace(' ', '-')}.txt",
            key=f"download-{section.title}",
        )


def _render_flashcards(body: str) -> None:
    cards = [block.strip() for block in body.split("\n\n") if block.strip()]
    for index, card in enumerate(cards, start=1):
        with st.container(border=True):
            st.markdown(f"**Card {index}**")
            st.write(card)


def _render_quiz(body: str) -> None:
    st.markdown(body)
    if st.button("Reveal answers", key=f"reveal-{hash(body)}"):
        st.info("Answer key is shown in the generated Answer Key section when available.")


def _tokens_for_length(output_length: str) -> int:
    return {"Short": 700, "Medium": 1200, "Long": 2200}[output_length]
