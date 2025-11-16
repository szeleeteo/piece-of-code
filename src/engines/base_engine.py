from abc import ABC, abstractmethod
from pathlib import Path

from streamlit.delta_generator import DeltaGenerator


class BaseEngine(ABC):
    """
    Abstract base class for code execution engines.

    All engines must define a language identifier and implement methods to
    execute/render code and list available examples.
    """

    @property
    @abstractmethod
    def language(self) -> str:
        """The programming language or format this engine supports (e.g., 'python', 'html')."""
        pass

    @abstractmethod
    def run(self, code: str, container: DeltaGenerator) -> None:
        """
        Executes or renders the provided code inside the given container.

        Args:
            code (str): The code to execute or render.
            container (DeltaGenerator): The Streamlit container to render output in.

        Returns:
            None
        """
        pass

    @abstractmethod
    def list_examples(self) -> list[Path]:
        """Lists available example files for this engine."""
        pass
