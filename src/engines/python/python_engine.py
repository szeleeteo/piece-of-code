from pathlib import Path

from ..python_base_engine import PythonBaseEngine


class PythonEngine(PythonBaseEngine):
    """Engine for executing Python code snippets."""

    def list_examples(self) -> list[Path]:
        """Lists available example files for this engine."""
        examples_dir = Path(__file__).parent / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            return list(examples_dir.glob("*.py"))
        return []
