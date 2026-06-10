# aigen_html

> **aigen** = AI + HTML generation — a forge for markup.

A portfolio project exploring AI-assisted web development. `aigen_html` is a small web server that uses a local [Ollama](https://ollama.ai) LLM to generate and edit HTML from natural language prompts — with JWT authentication, a live preview editor, and a separate frontend build pipeline.

I started this project to get hands-on experience with a range of tools and patterns I hadn't worked with before: serving a local LLM via API, hand-rolling JWT auth (no third-party library), building a minimal UI toolchain with Vite + Alpine.js, and structuring a Python project professionally from the ground up.

## Project Structure

```
aigen_html/
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
│   └── static/
│       └── pages/              # Legacy server-rendered HTML pages
│           ├── index.html      # Main editor (Alpine.js 2 via CDN)
│           └── login.html      # Login form
├── ui/                         # Modern Vite + Alpine.js 3 SPA
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
├── server.py                   # [DEPRECATED] Old root server, moved to src/
├── requirements.txt
└── requirements-dev.txt
```

## Architecture — Two Frontends

After a major refactor the project has **two separate frontends** that share the same backend API:

### Mode 1: Legacy Backend-Rendered (port 8080)

```
Browser → :8080 → Python http.server → serves static/pages/*.html directly
```

- User visits `http://localhost:8080/`
- Backend checks auth → if no cookie, redirects to `/login`
- User logs in → gets JWT cookie → redirected to `/`
- Backend serves `static/pages/index.html` with **Alpine.js 2 CDN**
- All HTML is server-rendered, Alpine adds reactivity on top

**Console log `INIT ALPINE !`** lives in this mode (static/index.html).

### Mode 2: Vite SPA (port 3000 + proxy to :8080)

```
Browser → :3000 → Vite dev server → /login, /create_html proxied to :8080
```

- User runs Vite dev server on port 3000
- Vite serves `ui/index.html` with **Alpine.js 3 (npm package)**
- API calls (`/login`, `/create_html`) are proxied to the backend
- The frontend is a pure SPA: login form, HTML editor, file save

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

# Optional: Vite frontend dependencies
cd ui
npm install
cd ..
```

### Run (choose one mode)

**Mode 1 — Backend only (port 8080):**
```bash
.venv\Scripts\activate
python -m aigen_html
```
Then visit `http://localhost:8080/` and log in with `test@test.de` / `test`.

**Mode 2 — Full stack with Vite dev server (port 3000):**
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

## Troubleshooting — Post-Refactor State

This project was recently restructured from flat files to a `src/` package layout.
If something doesn't work, check these known issues:

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: ollama_api` | Running old `server.py` instead of package | Use `python -m aigen_html` |
| Blank page on port 3000 | Vite index.html has no Alpine template yet | See `ui/index.html` — needs `x-data` markup |
| Redirect loop to /login | Missing `return` after serving pages (fixed) | Restart server |
| "users.json not found" | No `.env` file, using defaults | Harmless, copy `.env.example` to `.env` |
| Token doesn't work | Default expiry is 5 minutes | Increase `JWT_EXPIRE_SECONDS` |

## Technologies

- **Python 3.10+** — `http.server`, hand-rolled JWT, Ollama API integration
- **Alpine.js 2 & 3** — Legacy pages use v2 CDN, Vite SPA uses v3 npm package
- **Tailwind CSS** — Utility-first styling (CDN in legacy, via Vite in SPA)
- **Vite** — Frontend build tool with dev proxy
- **Ollama** — Local LLM inference
- **pytest / ruff / mypy** — Testing, linting, type checking
