from llama_index.core import Settings as LlamaSettings
from urllib.parse import urlparse
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CHROMA_HOST: str
    PORT_CHROMA: int
    CHROMA_DATA_DIR: Path
    CHROMA_COLLECTION: str
    PROJECT_DIR: Path
    PROJECT_PATH: Path
    OPENAI_API_KEY: str
    UI_MODE: str
    PORT_STREAMLIT: int
    PORT_GRADIO: int
    EMBEDDING_PROVIDER: str = "openai"  # デフォルト: openai

    @property
    def CHROMA_URL(self) -> str:
        return f"http://{self.CHROMA_HOST}:{self.PORT_CHROMA}"

    @property
    def CHROMA_PERSIST_DIR(self) -> Path:
        return self.CHROMA_DATA_DIR

    @property
    def INDEXED_FLAG_FILE(self) -> Path:
        return Path("/app/.last_indexed_commit")

    @property
    def WATCH_INTERVAL_SEC(self) -> int:
        return 1


cfg = Settings(_env_file=".env", _env_file_encoding="utf-8")
if cfg.EMBEDDING_PROVIDER.lower() == "openai":
    from llama_index.embeddings.openai import OpenAIEmbedding
    LlamaSettings.embed_model = OpenAIEmbedding()

# llama_index 設定
from llama_index.core import Settings as LlamaSettings

if cfg.EMBEDDING_PROVIDER.lower() == "openai":
    from llama_index.embeddings.openai import OpenAIEmbedding
    LlamaSettings.embed_model = OpenAIEmbedding()
    print("[CONFIG] Using OpenAIEmbedding")
else:
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {cfg.EMBEDDING_PROVIDER}")

# Debug 出力（任意）
print(f"[CONFIG] CHROMA_URL: {cfg.CHROMA_URL}")
print(f"[CONFIG] PROJECT_DIR: {cfg.PROJECT_DIR}")
print(f"[CONFIG] Embedding model: {LlamaSettings.embed_model}")
