from pathlib import Path

import streamlit as st

from ..python_base_engine import PythonBaseEngine


class StreamlitEngine(PythonBaseEngine):
    """Engine for executing Streamlit applications with access to Streamlit API."""

    def get_execution_globals(self) -> dict:
        """Inject Streamlit API into execution environment."""
        return {"__name__": "__main__", "st": st}

    def show_console_output(self, console: str) -> None:
        """Display console output in an expander if present."""
        console = console.strip()
        if console:
            with st.expander("Console output"):
                st.code(console, language="text")

    def list_examples(self) -> list[Path]:
        """Lists available example files for this engine."""
        examples_dir = Path(__file__).parent / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            return list(examples_dir.glob("*.py"))
        return []
