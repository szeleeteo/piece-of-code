import streamlit as st
from code_editor import code_editor

from config import (
    CODE_PREVIEW_THRESHOLD,
    CODE_PREVIEW_WIDTH,
    ENGINE_MAPPING,
    PYTHON_EDITOR_SETTINGS,
    TITLE,
    Engine,
    OutputLayout,
)
from engines import BaseEngine

st.set_page_config(
    page_title=TITLE, page_icon="⚡️", layout="wide", initial_sidebar_state="expanded"
)


if "output_layout" not in st.session_state:
    st.session_state.output_layout = OutputLayout.SIDE_BY_SIDE


def reset_code_selection():
    if "example_selector" in st.session_state and st.session_state.example_selector:
        st.session_state.example_selector = None


def get_panels():
    split_ratio = st.session_state.split_ratio
    reversed_split = CODE_PREVIEW_WIDTH - split_ratio
    should_max_left = split_ratio <= CODE_PREVIEW_THRESHOLD * CODE_PREVIEW_WIDTH
    should_max_right = split_ratio >= (1 - CODE_PREVIEW_THRESHOLD) * CODE_PREVIEW_WIDTH

    if should_max_left or should_max_right:
        st.session_state.output_layout = OutputLayout.TABS

        tab_order = ["Code", "Preview"]
        if st.session_state.swap_panels:
            tab_order = tab_order[::-1]  # reverse order to swap
            default_tab = "Preview" if should_max_right else "Code"
        else:
            default_tab = "Code" if should_max_right else "Preview"

        tabs = st.tabs(tab_order, default=default_tab)
        code_panel = tabs[tab_order.index("Code")]
        preview_panel = tabs[tab_order.index("Preview")]
    else:
        st.session_state.output_layout = OutputLayout.SIDE_BY_SIDE

        if st.session_state.swap_panels:
            preview_panel, code_panel = st.columns([split_ratio, reversed_split])
        else:
            code_panel, preview_panel = st.columns([split_ratio, reversed_split])

    return code_panel, preview_panel


def get_code(app_engine: BaseEngine) -> str:
    """
    Loads code from selected example file.

    Args:
        app_engine: The engine instance to get examples from.

    Returns:
        str: The code content from the selected example, or empty string.
    """
    code = ""

    try:
        examples = sorted(app_engine.list_examples())

        if examples:
            selected_ex = st.selectbox(
                "Examples",
                examples,
                format_func=lambda f: f.stem.title().replace("_", " "),
                key="example_selector",
            )
            if selected_ex:
                code = selected_ex.read_text()
    except Exception as e:
        st.error(f"Error loading examples: {e}")

    return code


def get_settings():
    """
    Configures sidebar settings and initializes the selected engine.

    Returns:
        tuple: (app_engine, code_panel, preview_panel, code) or None on error.
    """
    try:
        with st.sidebar:
            st.selectbox(
                "Engine",
                options=Engine,
                key="app_engine",
                on_change=reset_code_selection,
            )
            app_engine = ENGINE_MAPPING[st.session_state.app_engine]()

            code = get_code(app_engine)

            st.slider(
                "Resize Panels",
                min_value=int(CODE_PREVIEW_THRESHOLD * CODE_PREVIEW_WIDTH),
                max_value=int((1 - CODE_PREVIEW_THRESHOLD) * CODE_PREVIEW_WIDTH),
                value=CODE_PREVIEW_WIDTH // 2,
                key="split_ratio",
                format="",
            )
            st.toggle("Swap Panels", key="swap_panels")

        code_panel, preview_panel = get_panels()
        return app_engine, code_panel, preview_panel, code
    except Exception as e:
        st.error(f"Error initializing application: {e}")
        return None


def main():
    """Main application entry point."""
    st.title(TITLE)

    settings = get_settings()
    if settings is None:
        return

    app_engine, code_panel, preview_panel, code = settings

    try:
        with code_panel:
            if st.session_state.output_layout == OutputLayout.SIDE_BY_SIDE:
                st.write("Code")

            code_panel = st.container(border=True)
            with code_panel:
                editor_output = code_editor(
                    lang=app_engine.language, code=code, **PYTHON_EDITOR_SETTINGS
                )
                code = editor_output["text"]

        with preview_panel:
            if st.session_state.output_layout == OutputLayout.SIDE_BY_SIDE:
                st.write("Preview")

            preview_container = st.container(border=True, height="stretch")
            if code:
                app_engine.run(code, preview_container)
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.exception(e)


if __name__ == "__main__":
    main()
