"""Central configuration management using Pydantic Settings."""
from pathlib import Path
from pydantic_settings import BaseSettings
from llama_index.core import Settings as LlamaSettings


class Settings(BaseSettings):
    """Environment-driven configuration with type validation."""
    
    # Core Chroma settings
    CHROMA_HOST: str = "chroma"
    PORT_CHROMA: int = 8000
    CHROMA_DATA_DIR: str = "/chroma-data"
    CHROMA_COLLECTION: str = "source-code"
    
    # Application ports
    PORT_STREAMLIT: int = 8501
    PORT_GRADIO: int = 7860
    
    # Project paths
    PROJECT_DIR: str = "/workspace/project"
    PROJECT_PATH: str = "/home/user/myproject"
    
    # LLM settings
    OPENAI_API_KEY: str
    EMBEDDING_PROVIDER: str = "openai"
    UI_MODE: str = "streamlit"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def CHROMA_URL(self) -> str:
        """Generate Chroma URL from host and port."""
        return f"http://{self.CHROMA_HOST}:{self.PORT_CHROMA}"

    @property
    def CHROMA_PERSIST_DIR(self) -> Path:
        """Chroma persistence directory as Path object."""
        return Path(self.CHROMA_DATA_DIR)

    @property
    def INDEXED_FLAG_FILE(self) -> Path:
        """Flag file to track last indexed commit."""
        return Path("/app/.last_indexed_commit")

    @property
    def WATCH_INTERVAL_SEC(self) -> int:
        """File watcher polling interval."""
        return 1


# Global configuration instance
cfg = Settings()

# Configure LlamaIndex embedding model (once)
if cfg.EMBEDDING_PROVIDER.lower() == "openai":
    from llama_index.embeddings.openai import OpenAIEmbedding
    LlamaSettings.embed_model = OpenAIEmbedding()
    print(f"[CONFIG] Using OpenAIEmbedding")
else:
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {cfg.EMBEDDING_PROVIDER}")

# Debug output
print(f"[CONFIG] CHROMA_URL: {cfg.CHROMA_URL}")
print(f"[CONFIG] PROJECT_DIR: {cfg.PROJECT_DIR}")
print(f"[CONFIG] PROJECT_PATH: {cfg.PROJECT_PATH}")
print(f"[CONFIG] UI_MODE: {cfg.UI_MODE}")
print(f"[CONFIG] Embedding model: {LlamaSettings.embed_model}")
