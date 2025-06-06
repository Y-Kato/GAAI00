#!/usr/bin/env bash
# Git “dubious ownership” 回避
git config --global --add safe.directory "$PROJECT_DIR" || true
set -euo pipefail

echo "[run.sh] UI_MODE=${UI_MODE}"

# ① ファイルウォッチャをバックグラウンドで起動
python watcher.py &

# ② UI 起動
if [ "$UI_MODE" = "gradio" ]; then
  # Gradio は通常の Python 実行で OK
  python main.py --ui gradio
else
  # Streamlit は公式 CLI で起動する
  streamlit run ui_streamlit.py --server.port "$PORT_STREAMLIT"
fi
