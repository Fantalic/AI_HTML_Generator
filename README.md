# AI Creature Generator

An AI-powered HTML generator that uses local [Ollama](https://ollama.ai) models to create and edit HTML content from natural language prompts. Features JWT-based authentication and a live HTML preview editor.

## Project Structure

```
ai_creature_generator/
├── src/                          # Python package (src layout)
│   └── ai_creature_generator/
│       ├── __main__.py           # Entry point: python -m ai_creature_generator
│       ├── config.py             # Environment-based configuration
│       ├── server.py             # HTTP server & request routing
│       ├── exceptions.py         # Custom exceptions
│       ├── services/
│       │   ├── ollama.py         # Ollama API client
│       │   └── jwt.py            # JWT token creation & verification
│       ├── utils/
│       │   ├── html.py           # HTML extraction & think-tag removal
│       │   └── parsers.py        # Query string parser
│       └── static/pages/         # Server-rendered HTML templates
│           ├── index.html
│           └── login.html
├── ui/                           # Standalone UI sub-project (Vite + Alpine.js)
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── components/           # Reusable Alpine.js components
│       ├── services/             # API client layer
│       └── styles/               # CSS styles
├── tests/                        # Test suite (pytest)
├── data/                         # Seed data files
├── pyproject.toml                # Python packaging & tool config
├── Makefile                      # Common development tasks
└── requirements.txt              # Python dependencies
```

## Quick Start

### Backend

```bash
# Install dependencies
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
pip install -e .          # Install package in dev mode

# Run the server
python -m ai_creature_generator
```

Or use the convenience scripts:
```bash
install.bat    # Creates venv & installs deps
run.bat        # Starts the server
```

### UI Sub-project (optional)

```bash
cd ui
npm install
npm run dev    # Starts Vite dev server on port 3000
```

## Development

```bash
make install    # Install package + dev deps
make run        # Start server
make test       # Run tests
make lint       # Lint with ruff
make format     # Format with ruff
```

## Configuration

Copy `.env.example` to `.env` and adjust:

| Variable | Default | Description |
|---|---|---|
| `SERVER_PORT` | `8080` | HTTP server port |
| `JWT_SECRET` | `geheimer_schluessel` | JWT signing key |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `JWT_EXPIRE_SECONDS` | `300` | Token lifetime |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_DEFAULT_MODEL` | `deepseek-r1:8b` | Default LLM model |

## Technologies

- **Python 3.10+** — Built-in `http.server`, JWT (hand-rolled), Ollama API
- **Alpine.js** — Reactive UI components
- **Tailwind CSS** — Utility-first styling
- **Vite** — Frontend build tool (UI sub-project)
- **Ollama** — Local LLM inference
