# aigen_html

> **aigen** = AI + HTML generation — a forge for markup.

A portfolio project exploring AI-assisted web development. `aigen_html` is a small web server that uses a local [Ollama](https://ollama.ai) LLM to generate and edit HTML from natural language prompts — with JWT authentication, a live preview editor, and a separate frontend build pipeline.

I started this project to get hands-on experience with a range of tools and patterns I hadn't worked with before: serving a local LLM via API, hand-rolling JWT auth (no third-party library), building a minimal UI toolchain with Vite + Alpine.js, and structuring a Python project professionally from the ground up.

## Project Structure

```
├── src/aigen_html/             # Python package (backend)
│   ├── __init__.py
│   ├── __main__.py             # Entry: python -m aigen_html
│   ├── config.py               # Env-based configuration
│   ├── server.py               # HTTP server & request routing
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ollama.py           # Ollama API client
│   │   └── jwt.py              # JWT creation & verification
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── html.py             # HTML extraction & think-tag removal
│   │   └── parsers.py          # Query string parser
├── ui/                         # Vite + Alpine.js 3 SPA (single frontend)
│   ├── package.json
│   ├── vite.config.js          # Dev server :3000, proxies API to :8080
│   ├── index.html              # SPA entry point
│   └── src/
│       ├── main.js             # Alpine.js 3 boot + component registration
│       ├── components/
│       │   ├── loginForm.js    # Login form logic
│       │   ├── htmlEditor.js   # HTML editor + generation
│       │   └── fileSaver.js    # Save-to-file logic
│       ├── services/
│       │   └── api.js          # Backend API client
│       └── styles/
│           └── main.css
├── tests/                      # pytest suite
├── data/
│   └── users.json              # User credentials (test@test.de / test)
├── pyproject.toml              # Python packaging & tool config
├── Makefile                    # Dev tasks
├── requirements.txt
└── requirements-dev.txt
```

## Architecture — SPA Frontend

The frontend is a single-page application built with Vite + Alpine.js 3.

```
Browser → :8080 → Python backend serves ui/dist/ (built SPA)
Browser → :3000 → Vite dev server proxies /login, /create_html to :8080
```

- **Production mode**: Backend on port 8080 serves the built SPA from `ui/dist/`
- **Development mode**: Vite dev server on port 3000 with hot reload, proxying API calls to the backend
- The SPA handles login and the HTML editor entirely on the client side

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for Vite frontend)
- Ollama (optional, for AI generation)

### Setup

```bash
git clone <repo>
cd aigen_html

# Python virtual environment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

# Build the frontend
cd ui
npm install
npm run build
cd ..
```

### Run

```bash
.venv\Scripts\activate
python -m aigen_html
```
Then visit `http://localhost:8080/` and log in with `test@test.de` / `test`.

For development with hot reload, run the Vite dev server alongside:

```bash
# Terminal 1: Backend
.venv\Scripts\activate
python -m aigen_html

# Terminal 2: Vite frontend
cd ui
npm run dev
```
Then visit `http://localhost:3000/`.

## Configuration

Copy `.env.example` to `.env` and adjust:

| Variable | Default | Description |
|---|---|---|
| `SERVER_PORT` | `8080` | Backend HTTP server port |
| `JWT_SECRET` | `geheimer_schluessel` | JWT signing key |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `JWT_EXPIRE_SECONDS` | `300` | Token lifetime (5 min) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_DEFAULT_MODEL` | `deepseek-r1:8b` | Default LLM model |

## Development

```bash
make install    # Install package + dev deps
make run        # Start server
make test       # Run tests
make lint       # Lint with ruff
make format     # Format with ruff
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: ollama_api` | Running old `server.py` instead of package | Use `python -m aigen_html` |
| "users.json not found" | No `.env` file, using defaults | Harmless, copy `.env.example` to `.env` |
| Token doesn't work | Default expiry is 5 minutes | Increase `JWT_EXPIRE_SECONDS` |

## Technologies

- **Python 3.10+** — `http.server`, hand-rolled JWT, Ollama API integration
- **Alpine.js 3** — Reactive frontend via npm package
- **Tailwind CSS** — Utility-first styling via CDN
- **Vite** — Frontend build tool with dev proxy
- **Ollama** — Local LLM inference
- **pytest / ruff / mypy** — Testing, linting, type checking
