# Piece of Code

[![Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://piece-of-code.streamlit.app//)

An interactive code playground built with Streamlit that lets you write and execute code snippets in multiple languages with live preview.

## Features

- **Multi-language Support**: Python, Streamlit, HTML/CSS/JavaScript, and React/TypeScript
- **Live Preview**: See your code results in real-time
- **Split Panel Interface**: Adjustable side-by-side or tabbed layout
- **Code Editor**: Syntax highlighting, auto-completion, and keyboard shortcuts (Cmd/Ctrl+Enter to run)
- **Example Gallery**: Pre-built examples for each language to get you started
- **Safety Constraints**: Basic sandboxing for Python code execution

## Supported Languages

1. **Python**: Execute Python code snippets with console output capture
2. **Streamlit**: Build interactive Streamlit apps with full API access
3. **HTML/CSS/JavaScript**: Create web visualizations and animations
4. **React/TypeScript**: Build React components with TypeScript support

## Requirements

- **Python**: >=3.11
- **uv**: Fast Python package installer and resolver
- **make**: Build automation tool

## Quick Start

### Installation

```sh
make init  # Initialize virtual environment and install dependencies
```

### Running the Application

```sh
make dev  # Start Streamlit with auto-reload
```

The app will be available at `http://localhost:8501`

### Code Quality

```sh
make check  # Run pre-commit hooks (linting and formatting)
```

### Cleanup

```sh
make clean  # Remove virtual environment and caches
```

## Architecture

The application uses a plugin-based architecture where each language is implemented as a separate engine class. All engines inherit from `BaseEngine` and implement:

- `language`: Returns the language identifier for syntax highlighting
- `run(code, container)`: Executes/renders code in a Streamlit container
- `list_examples()`: Returns available example files

See [CLAUDE.md](CLAUDE.md) for detailed architecture documentation.

## Adding New Engines

1. Create a new directory under `src/engines/{engine_name}/`
2. Implement an engine class inheriting from `BaseEngine`
3. Register it in `src/config.py` (add to `Engine` enum and `ENGINE_MAPPING`)
4. Add example files in `src/engines/{engine_name}/examples/`
5. Export from `src/engines/__init__.py`

## Safety

- **Python/Streamlit**: Blocks imports of dangerous packages (os, sys, subprocess, etc.)
- **JavaScript/React**: Browser-level sandboxing via iframe

⚠️ **Warning**: This is not a comprehensive sandbox. Do not execute untrusted code.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


