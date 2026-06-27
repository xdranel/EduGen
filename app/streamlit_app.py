from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from edugen.config.logging_config import configure_logging
from edugen.config.settings import AppSettings
from edugen.ui.pages import render_page


def main() -> None:
    settings = AppSettings()
    configure_logging(settings)

    st.set_page_config(
        page_title=settings.app_name,
        page_icon=":books:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title(settings.app_name)
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Generate", "History", "Downloads", "Settings", "About"],
    )
    st.sidebar.caption(f"Version {settings.version}")
    st.sidebar.caption("Model: not configured")

    render_page(page, settings)


if __name__ == "__main__":
    main()
