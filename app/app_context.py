"""Create & expose global retriever and LLM objects."""
from pathlib import Path
from urllib.parse import urlparse

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient
from langchain.chat_models import ChatOpenAI

from config import cfg
from indexer import build_full_index

# ===== デバッグコードをここに追加 =====
print(f"[DEBUG] PROJECT_DIR exists: {Path(cfg.PROJECT_DIR).exists()}")
if Path(cfg.PROJECT_DIR).exists():
    files = list(Path(cfg.PROJECT_DIR).iterdir())[:5]
    print(f"[DEBUG] Files in PROJECT_DIR: {files}")
    print(f"[DEBUG] Total files: {len(list(Path(cfg.PROJECT_DIR).rglob('*')))}")
# =====================================

# ---- index & retriever -------------------------------------------------
if not Path(cfg.INDEXED_FLAG_FILE).exists():
    build_full_index()

url = urlparse(cfg.CHROMA_URL)
chroma_client = HttpClient(host=url.hostname, port=url.port)
collection = chroma_client.get_or_create_collection(name=cfg.CHROMA_COLLECTION)

vector_store = ChromaVectorStore(
    chroma_collection=collection,
    collection_name=cfg.CHROMA_COLLECTION,
    persist_dir=str(cfg.CHROMA_PERSIST_DIR),
    host=url.hostname,
    port=url.port,
)
index = VectorStoreIndex.from_vector_store(vector_store)
retriever = index.as_retriever(search_kwargs={"k": 6})

# ---- LLM ---------------------------------------------------------------
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

"""`retriever` と `llm` を他モジュールが import して使用する想定"""
