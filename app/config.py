import os
from pathlib import Path
from urllib.parse import urlparse

# 環境変数ベース設定（Docker 環境想定）
CHROMA_URL = os.environ.get("CHROMA_URL")
url = urlparse(CHROMA_URL)
CHROMA_HOST = url.hostname
PORT_CHROMA = url.port

PROJECT_DIR = Path(os.environ.get("PROJECT_DIR"))
CHROMA_COLLECTION = os.environ.get("CHROMA_COLLECTION")
CHROMA_PERSIST_DIR = Path(os.environ.get("CHROMA_DATA_DIR"))

# 内部動作用定数
INDEXED_FLAG_FILE = Path("/app/.last_indexed_commit")
WATCH_INTERVAL_SEC = 1
print(f"[CONFIG] PORT_CHROMA raw: {os.environ.get('PORT_CHROMA')!r}")
print(f"[CONFIG] CHROMA_URL: {CHROMA_URL}")
print(f"[CONFIG] CHROMA_HOST: {CHROMA_HOST}")
print(f"[CONFIG] PORT_CHROMA: {PORT_CHROMA}")

# モデル指定
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
Settings.embed_model = OpenAIEmbedding()
print(f"[CONFIG] Embedding model set: {Settings.embed_model}")