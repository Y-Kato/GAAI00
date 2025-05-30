#!/usr/bin/env bash

# Git リポジトリが “dubious ownership” で止まる場合読み取り専用マウントでも許可
git config --global --add safe.directory "$PROJECT_DIR" || true

set -euo pipefail

# 1️⃣  Kick off background file‑watcher for incremental updates
python watcher.py &

# 2️⃣  Launch UI (defaults to Streamlit)
if [ "$UI_MODE" = "gradio" ]; then
  python main.py --ui gradio
else
  streamlit run main.py --server.port 8501 -- --ui streamlit
fi