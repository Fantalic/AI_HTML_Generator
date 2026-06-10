import os
from pathlib import Path

JWT_SECRET = os.getenv("JWT_SECRET", "geheimer_schluessel")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_SECONDS = int(os.getenv("JWT_EXPIRE_SECONDS", "300"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "deepseek-r1:8b")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

USER_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users.json"
STATIC_DIR = Path(__file__).resolve().parent / "static"
