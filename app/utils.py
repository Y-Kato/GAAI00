import os
from pathlib import Path

CHROMA_COLLECTION = "source-code"
CHROMA_PERSIST_DIR = Path("/chroma-data")
PROJECT_DIR = Path(os.environ.get("PROJECT_DIR", "/workspace/project"))
CHROMA_URL = os.environ.get("CHROMA_URL", "http://localhost:8000")