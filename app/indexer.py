"""Full & partial indexing of the mounted project into Chroma via LlamaIndex."""
from pathlib import Path
from typing import Sequence, List

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient

from utils import PROJECT_DIR, CHROMA_COLLECTION, CHROMA_URL, CHROMA_PERSIST_DIR

# --- vector store -----------------------------------------------------------

def _get_vs():
    client = HttpClient(host="chroma", port=8000)
    return ChromaVectorStore(
        client=client, collection_name=CHROMA_COLLECTION, persist_dir=str(CHROMA_PERSIST_DIR)
    )


def build_full_index() -> VectorStoreIndex:
    docs = SimpleDirectoryReader(str(PROJECT_DIR)).load_data()
    vs = _get_vs()
    index = VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vs))
    index.storage_context.persist()
    return index

# ---------------------------------------------------------------------------

# 🤏 **Partial update** when a subset of files changed -----------------------

INDEXED_FLAG_FILE = Path("/app/.last_indexed_commit")


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