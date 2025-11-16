import ast
import contextlib
import io
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from src.engines.base_engine import BaseEngine

DISALLOWED_PYTHON_PACKAGES = frozenset(
    {"os", "sys", "subprocess", "shutil", "pathlib", "socket"}
)


class PythonEngine(BaseEngine):
    """Builder for Streamlit Python applications."""

    @property
    def language(self) -> str:
        return "python"

    def run(self, code: str, container: DeltaGenerator) -> None:
        """
        Executes the provided Streamlit script inside the given result container,
        after performing basic safety checks.

        Args:
            script (str): The Python script to execute.
            result_container (DeltaGenerator): The Streamlit container to render output in.

        Returns:
            None
        """
        ok, msg = self._basic_safety_check(code)

        if not ok:
            st.error(msg)
        else:
            with container:
                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    try:
                        glb = {"__name__": "__main__"}
                        exec(code, glb, None)
                    except Exception as e:
                        st.exception(e)
                    finally:
                        console = output_buffer.getvalue()
                        st.code(console, language="text", wrap_lines=True)

    def _basic_safety_check(self, src: str) -> tuple[bool, str]:
        """
        Checks the provided Python source code for forbidden imports.

        Args:
            src (str): The source code to check.

        Returns:
            tuple[bool, str]: (True, "") if safe, (False, reason) if unsafe.
        """
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if any(
                    alias.name.split(".")[0] in DISALLOWED_PYTHON_PACKAGES
                    for alias in node.names
                ):
                    return False, "Blocked: forbidden import used."
            elif isinstance(node, ast.ImportFrom):
                if (node.module or "").split(".")[0] in DISALLOWED_PYTHON_PACKAGES:
                    return False, "Blocked: forbidden import used."
        return True, ""

    def list_examples(self) -> list[Path]:
        """Lists available example files for this builder."""
        examples_dir = Path(__file__).parent / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            return list(examples_dir.glob("*.py"))
        return []
