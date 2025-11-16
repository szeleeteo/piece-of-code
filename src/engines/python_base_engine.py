import ast
import contextlib
import io
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from .base_engine import BaseEngine

DISALLOWED_PYTHON_PACKAGES = frozenset(
    {"os", "sys", "subprocess", "shutil", "pathlib", "socket"}
)


class PythonBaseEngine(BaseEngine):
    """
    Base class for Python-based engines (Python and Streamlit).
    Handles safety checks and execution logic.
    """

    @property
    def language(self) -> str:
        return "python"

    def get_execution_globals(self) -> dict:
        """
        Returns the global variables to inject into exec().
        Override this method to customize the execution environment.
        """
        return {"__name__": "__main__"}

    def show_console_output(self, console: str) -> None:
        """
        Displays console output.
        Override this method to customize how console output is shown.
        """
        st.code(console, language="text", wrap_lines=True)

    def run(self, code: str, container: DeltaGenerator) -> None:
        """
        Executes the provided Python code inside the given container,
        after performing basic safety checks.

        Args:
            code (str): The Python code to execute.
            container (DeltaGenerator): The Streamlit container to render output in.

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
                        glb = self.get_execution_globals()
                        exec(code, glb, None)
                    except Exception as e:
                        st.exception(e)
                    finally:
                        console = output_buffer.getvalue()
                        if console:
                            self.show_console_output(console)

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
        """
        Lists available example files for this engine.

        Note: This default implementation won't work correctly. Subclasses should override
        this method to return their own examples.
        """
        return []
