import streamlit as st

from edugen.config.settings import AppSettings
from edugen.core.exceptions import format_error
from edugen.core.validation import validate_topic


def render_page(page: str, settings: AppSettings) -> None:
    pages = {
        "Home": _home_page,
        "Generate": _generate_page,
        "History": _history_page,
        "Downloads": _downloads_page,
        "Settings": _settings_page,
        "About": _about_page,
    }
    pages.get(page, _home_page)(settings)


def _home_page(settings: AppSettings) -> None:
    st.title(settings.app_name)
    st.subheader(settings.tagline)
    st.write(
        "EduGen AI will generate structured learning materials from one topic "
        "using open-source generative AI models."
    )

    col1, col2, col3 = st.columns(3)
    col1.info("Learning materials")
    col2.info("Quizzes and flashcards")
    col3.info("Export and history")

    st.markdown("### Architecture")
    st.write("Python modular monolith with Streamlit, SQLite, and a future local LLM pipeline.")


def _generate_page(settings: AppSettings) -> None:
    st.title("Generate Learning Material")
    st.caption("Foundation placeholder. AI generation is planned for Prompt 3.")

    with st.form("generate_form"):
        topic = st.text_input("Topic")
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        language = st.selectbox("Language", ["English", "Indonesian"])
        submitted = st.form_submit_button("Validate Topic")

    if submitted:
        try:
            cleaned = validate_topic(topic)
        except ValueError as error:
            st.error(format_error(error))
        else:
            st.success(f"Topic accepted: {cleaned}")
            st.write(f"Difficulty: {difficulty}")
            st.write(f"Language: {language}")


def _history_page(settings: AppSettings) -> None:
    st.title("History")
    st.info("Generation history will be stored with SQLite in a later phase.")


def _downloads_page(settings: AppSettings) -> None:
    st.title("Downloads")
    st.info("PDF, Markdown, TXT, and HTML exports will be added after generation exists.")


def _settings_page(settings: AppSettings) -> None:
    st.title("Settings")
    st.text_input("Model", value="Not configured", disabled=True)
    st.selectbox("Theme", ["Light", "Dark"])
    st.selectbox("Default language", ["English", "Indonesian"])


def _about_page(settings: AppSettings) -> None:
    st.title("About")
    st.write(settings.tagline)
    st.write(f"Version: {settings.version}")
    st.write("License: MIT")
    st.write("Authors: to be completed")
