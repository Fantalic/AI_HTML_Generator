import os
from pathlib import Path

JWT_SECRET = os.getenv("JWT_SECRET", "geheimer_schluessel")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_SECONDS = int(os.getenv("JWT_EXPIRE_SECONDS", "300"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "qwen3-coder:480b-cloud")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
USER_DATA_PATH = PROJECT_ROOT / "data" / "users.json"
UI_DIST_DIR = PROJECT_ROOT / "ui" / "dist"
