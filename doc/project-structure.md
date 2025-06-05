# Project Structure & Conventions

> **All configuration flows through `.env → config.py`**. Hard‑coded values are treated as bugs.

```
GAAI00/
├── app/
│   ├── config.py        # central .env resolver
│   ├── ui_streamlit.py  # ↳ UI entry (streamlit)
│   ├── ui_gradio.py     # ↳ UI entry (gradio)
│   ├── indexer.py       # builds/updates Chroma
│   ├── watcher.py       # inotify incremental watcher
│   ├── git_utils.py     # Git history & blame helpers
│   ├── Dockerfile
│   └── run.sh           # boot script (env → config → watcher → UI)
│
├── docker-compose.yml   # single-node stack (app + chroma)
├── .env.example         # **canonical list of variables**
├── chroma_data/         # Chroma persistence (bind‑mount)
├── docs/                # this folder
└── etc/
```

---

## Mandatory Conventions

1. **No direct `os.getenv()` outside `config.py`.**
   Import `from app.config import cfg` and read from `cfg.CHROMA_URL`, etc.
2. **All new variables → `.env.example` → `config.py`.**
   PR fails if CI detects missing keys.
3. **Generated assets** (`chroma_data`, `*.log`) must be excluded via `.gitignore`.

---

## `config.py` Anatomy (excerpt)

```python
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    CHROMA_HOST: str = "chroma"
    PORT_CHROMA: int = 8000
    # ... other fields ...

    @property
    def CHROMA_URL(self):
        return f"http://{self.CHROMA_HOST}:{self.PORT_CHROMA}"

cfg = Settings(_env_file=".env", _env_file_encoding="utf-8")
```

This pattern guarantees:

* Single import cost
* Auto‑completion & type safety
* Late evaluation (overridden easily in tests)

---

## Git Policy

* **feature/<name>** → PR → main
* Doc updates belong in the same PR as code changes that introduce new env vars.
* CI enforces `docs/project-structure.md` checksum to notice silent drifts.
