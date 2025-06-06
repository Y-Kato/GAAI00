from pathlib import Path
from typing import List
from urllib.parse import urlparse

from config import cfg
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient

def _get_vs():
    url = urlparse(cfg.CHROMA_URL)
    print(f"[INDEXER] Using CHROMA_URL: {cfg.CHROMA_URL}, host: {url.hostname}, port: {url.port}")

    client = HttpClient(host=url.hostname, port=url.port)

    try:
        collection = client.get_or_create_collection(name=cfg.CHROMA_COLLECTION)
    except Exception as e:
        if "already exists" in str(e):
            print(f"[WARN] Collection already exists. Retrieving instead.")
            collection = client.get_collection(name=cfg.CHROMA_COLLECTION)
        else:
            raise

    return ChromaVectorStore(
        chroma_collection=collection,
        collection_name=cfg.CHROMA_COLLECTION,
        persist_dir=str(cfg.CHROMA_PERSIST_DIR),
        host=url.hostname,
        port=url.port
    )

def build_full_index() -> VectorStoreIndex:
    print("[INDEXER] 🟡 build_full_index START")
    print(f"[INDEXER] 📁 PROJECT_DIR = {cfg.PROJECT_DIR}")
    print(f"[INDEXER] 📄 Listing files in PROJECT_DIR:")
    for f in Path(cfg.PROJECT_DIR).rglob("*"):
        print("   -", f)
    print("[INDEXER] 🗂️ Full index build started.")
    docs = SimpleDirectoryReader(str(cfg.PROJECT_DIR)).load_data()
    print(f"[INDEXER] ✅ Loaded {len(docs)} documents.")

    vs = _get_vs()
    index = VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vs))
    
    # 🔥 重要: ローカルストレージへの保存を削除
    # index.storage_context.persist()  # ← この行を削除（Chromaのみ使用）
    
    print("[INDEXER] 📦 Index built and stored in Chroma (no local storage).")
    return index

def _list_changed_files(last_commit: str) -> List[Path]:
    import git

    repo = git.Repo(str(cfg.PROJECT_DIR))
    diff = repo.git.diff("--name-only", last_commit, "HEAD").splitlines()
    return [cfg.PROJECT_DIR / p for p in diff if (cfg.PROJECT_DIR / p).is_file()]

def incremental_update():
    import git

    repo = git.Repo(str(cfg.PROJECT_DIR))
    head = repo.head.commit.hexsha

    if cfg.INDEXED_FLAG_FILE.exists():
        last_commit = cfg.INDEXED_FLAG_FILE.read_text().strip()
        if last_commit == head:
            return  # nothing new
        changed = _list_changed_files(last_commit)
    else:
        changed = []

    if not changed:
        docs = []
    else:
        reader = SimpleDirectoryReader(input_files=[str(p) for p in changed])
        docs = reader.load_data()

    if docs:
        vs = _get_vs()
        VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vs))
        # 🔥 重要: ローカルストレージへの保存を削除
        # vs.persist()  # ← この行を削除（Chromaが自動保存）

    cfg.INDEXED_FLAG_FILE.write_text(head)
    