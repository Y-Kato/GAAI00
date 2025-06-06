"""Create & expose global retriever and LLM objects."""
from pathlib import Path
from urllib.parse import urlparse

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient
from langchain.chat_models import ChatOpenAI  # 固定バージョンなので既存インポートを維持

from config import cfg
from indexer import build_full_index

# ===== デバッグコードをここに追加 =====
print(f"[DEBUG] PROJECT_DIR exists: {Path(cfg.PROJECT_DIR).exists()}")
if Path(cfg.PROJECT_DIR).exists():
    files = list(Path(cfg.PROJECT_DIR).iterdir())[:5]
    print(f"[DEBUG] Files in PROJECT_DIR: {files}")
    print(f"[DEBUG] Total files: {len(list(Path(cfg.PROJECT_DIR).rglob('*')))}")
# =====================================

def _check_collection_exists_and_populated():
    """Chromaコレクションが存在し、ドキュメントが含まれているかチェック"""
    try:
        url = urlparse(cfg.CHROMA_URL)
        client = HttpClient(host=url.hostname, port=url.port)
        collection = client.get_collection(cfg.CHROMA_COLLECTION)
        count = collection.count()
        print(f"[app_context] Collection '{cfg.CHROMA_COLLECTION}' has {count} documents")
        return count > 0
    except Exception as e:
        print(f"[app_context] Collection check failed: {e}")
        return False

def _initialize_index():
    """インデックスの初期化（必要に応じて構築）"""
    # 1. フラグファイルとコレクションの両方をチェック
    flag_exists = Path(cfg.INDEXED_FLAG_FILE).exists()
    collection_populated = _check_collection_exists_and_populated()
    
    print(f"[app_context] Flag file exists: {flag_exists}")
    print(f"[app_context] Collection populated: {collection_populated}")
    
    # 2. どちらかが欠けている場合は再構築
    if not flag_exists or not collection_populated:
        print("[app_context] 🟡 Building/rebuilding full index...")
        build_full_index()
        print("[app_context] ✅ Index build completed")
    else:
        print("[app_context] ✅ Index already exists and populated")

# ---- index & retriever -------------------------------------------------
_initialize_index()

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

print("[app_context] 🎉 Global context initialized successfully")

"""`retriever` と `llm` を他モジュールが import して使用する想定"""