from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit.delta_generator import DeltaGenerator

from ..base_engine import BaseEngine


class ReactEngine(BaseEngine):
    """Engine for rendering React applications using TypeScript."""

    @property
    def language(self) -> str:
        return "typescript"

    def run(self, code: str, container: DeltaGenerator) -> None:
        """
        Renders the provided React TypeScript code inside the given container.

        The code is wrapped in a complete HTML document with React, ReactDOM, and Babel
        loaded from CDN. The TypeScript code is transpiled to JavaScript in the browser.

        Args:
            code (str): The React TypeScript code to render.
            container (DeltaGenerator): The Streamlit container to render output in.

        Returns:
            None
        """
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React TypeScript App</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        #root {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" data-type="module">
{code}
    </script>
</body>
</html>
"""
        with container:
            try:
                components.html(html_template, height=800, scrolling=True)
            except Exception as e:
                st.error(f"Error rendering React TypeScript: {e}")
                st.exception(e)

    def list_examples(self) -> list[Path]:
        """Lists available example files for this engine."""
        examples_dir = Path(__file__).parent / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            return list(examples_dir.glob("*.tsx"))
        return []
