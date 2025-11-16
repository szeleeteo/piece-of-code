from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit.delta_generator import DeltaGenerator

from ..base_engine import BaseEngine


class JSEngine(BaseEngine):
    """Engine for rendering HTML/CSS/JavaScript applications."""

    @property
    def language(self) -> str:
        return "html"

    def run(self, code: str, container: DeltaGenerator) -> None:
        """
        Renders the provided HTML/CSS/JavaScript code inside the given container.

        Args:
            code (str): The HTML/CSS/JavaScript code to render.
            container (DeltaGenerator): The Streamlit container to render output in.

        Returns:
            None
        """
        with container:
            try:
                components.html(code, height=640, scrolling=True)
            except Exception as e:
                st.error(f"Error rendering HTML/CSS/JavaScript: {e}")
                st.exception(e)

    def list_examples(self) -> list[Path]:
        """Lists available example files for this engine."""
        examples_dir = Path(__file__).parent / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            return list(examples_dir.glob("*.html"))
        return []
