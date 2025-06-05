"""Full & partial indexing of the mounted project into Chroma via LlamaIndex."""
from pathlib import Path
from typing import Sequence, List
from urllib.parse import urlparse
from config import PROJECT_DIR, CHROMA_COLLECTION, CHROMA_URL, CHROMA_PERSIST_DIR, INDEXED_FLAG_FILE

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient

# --- vector store -----------------------------------------------------------

def _get_vs():
    url = urlparse(CHROMA_URL)
    print(f"[INDEXER] Using CHROMA_URL: {CHROMA_URL}, host: {url.hostname}, port: {url.port}")

    client = HttpClient(host=url.hostname, port=url.port)

    try:
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    except Exception as e:
        if "already exists" in str(e):
            print(f"[WARN] Collection already exists. Retrieving instead.")
            collection = client.get_collection(name=CHROMA_COLLECTION)
        else:
            raise

    return ChromaVectorStore(
        chroma_collection=collection,
        collection_name=CHROMA_COLLECTION,
        persist_dir=str(CHROMA_PERSIST_DIR),
        host=url.hostname,
        port=url.port
    )

def build_full_index() -> VectorStoreIndex:
    docs = SimpleDirectoryReader(str(PROJECT_DIR)).load_data()
    vs = _get_vs()
    index = VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vs))
    index.storage_context.persist()
    return index

# ---------------------------------------------------------------------------

# 🤏 **Partial update** when a subset of files changed -----------------------

def _list_changed_files(last_commit: str) -> List[Path]:
    import git

    repo = git.Repo(str(PROJECT_DIR))
    diff = repo.git.diff("--name-only", last_commit, "HEAD").splitlines()
    return [PROJECT_DIR / p for p in diff if (PROJECT_DIR / p).is_file()]


def incremental_update():
    import git

    repo = git.Repo(str(PROJECT_DIR))
    head = repo.head.commit.hexsha

    if INDEXED_FLAG_FILE.exists():
        last_commit = INDEXED_FLAG_FILE.read_text().strip()
        if last_commit == head:
            return  # nothing new
        changed = _list_changed_files(last_commit)
    else:
        changed = []

    if not changed:
        docs = []  # just commit metadata maybe
    else:
        reader = SimpleDirectoryReader(input_files=[str(p) for p in changed])
        docs = reader.load_data()

    if docs:
        vs = _get_vs()
        VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vs))
        vs.persist()

    INDEXED_FLAG_FILE.write_text(head)