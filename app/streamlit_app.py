from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from edugen.config.logging_config import configure_logging
from edugen.config.settings import AppSettings
from edugen.storage.sqlite import initialize_database
from edugen.ui.pages import render_page


def main() -> None:
    settings = AppSettings()
    configure_logging(settings)
    initialize_database(settings.database_path)

    st.set_page_config(
        page_title=settings.app_name,
        page_icon=":books:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title(settings.app_name)
    st.sidebar.caption(settings.tagline)
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Generate Learning Material", "History", "Downloads", "Settings", "About"],
    )
    st.sidebar.divider()
    st.sidebar.caption("Current model")
    st.sidebar.code(st.session_state.get("model_id", "Qwen/Qwen2.5-0.5B-Instruct"))
    st.sidebar.caption(f"Theme: {st.session_state.get('theme', 'Light')}")
    st.sidebar.caption(f"Language: {st.session_state.get('language', 'English')}")
    st.sidebar.caption(f"Version {settings.version}")
    if st.sidebar.button("Clear current result"):
        st.session_state.pop("last_result", None)
        st.rerun()

    render_page(page, settings)


if __name__ == "__main__":
    main()
