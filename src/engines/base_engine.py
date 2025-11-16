from abc import ABC, abstractmethod
from pathlib import Path

from streamlit.delta_generator import DeltaGenerator


class BaseEngine(ABC):
    """
    Abstract base class for code builders.

    All builders must define a language, default code, and implement a build method
    that executes/renders the script in the provided container.
    """

    @property
    @abstractmethod
    def language(self) -> str:
        """The programming language or format this builder supports (e.g., 'python', 'html')."""
        pass

    @abstractmethod
    def run(self, code: str, result_container: DeltaGenerator) -> None:
        """
        Executes or renders the provided script inside the given result container.

        Args:
            script (str): The code/script to execute or render.
            result_container (DeltaGenerator): The Streamlit container to render output in.

        Returns:
            None
        """
        pass

    @abstractmethod
    def list_examples(self) -> list[Path]:
        """Lists available example files for this builder."""
        pass
