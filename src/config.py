from enum import StrEnum

from engines import JSEngine, PythonEngine, ReactEngine, StreamlitEngine

TITLE = "Piece of Code"
CODE_PREVIEW_WIDTH = 10
CODE_PREVIEW_THRESHOLD = 0.2


class OutputLayout(StrEnum):
    SIDE_BY_SIDE = "side-by-side"
    TABS = "tabs"


class Engine(StrEnum):
    PYTHON = "Python"
    STREAMLIT = "Streamlit"
    JS = "HTML/CSS/JavaScript"
    REACT = "React (TypeScript)"


ENGINE_MAPPING = {
    Engine.PYTHON: PythonEngine,
    Engine.STREAMLIT: StreamlitEngine,
    Engine.JS: JSEngine,
    Engine.REACT: ReactEngine,
}


run_button_settings = {
    "name": "Run",
    "feather": "Play",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "alwaysOn": True,
    "style": {"bottom": "0.44rem", "right": "0.4rem"},
    "bindKey": {"win": "Ctrl-Enter", "mac": "Command-Enter"},
}


PYTHON_EDITOR_SETTINGS = {
    "height": [24, 24],  # lines
    "focus": True,
    "buttons": [run_button_settings],
    "props": {
        "enableBasicAutocompletion": True,
        "enableLiveAutocompletion": True,
        "enableSnippets": False,
    },
    "options": {"showLineNumbers": True, "wrap": True},
}
