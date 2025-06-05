![CI](https://github.com/Y-Kato/GAAI00/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/github/license/Y-Kato/GAAI00)
![Last Commit](https://img.shields.io/github/last-commit/Y-Kato/GAAI00)

# LlamaIndex + LangChain Dev‑Assistant Stack (Docker Compose)

> 🦙🔗 **コード解析・リファクタ支援 ＆ マルチプロジェクト対応のポータブル環境**
>
> ⚠️ **このスタックは構築中の素体です。LangChain の Agent 化や Tool 呼び出しの導入は今後の拡張対象であり、現時点では主にインデックス構築と検索支援に特化しています。**
>
> 本スタックは *LlamaIndex* と *LangChain* を中心に、Git 履歴・ソースツリーから得られる情報を組み合わせて開発を支援する AI ツールチェーンです。Docker 1 コマンドで起動でき、Streamlit / Gradio UI を選択可能。増分インデックス更新や永続型ベクトルストア (Chroma) を含みます。

---

## ✨ 主なポイント

| 機能                           | 説明                                                             |
| ------------------------------ | ---------------------------------------------------------------- |
| **🗄️ Chroma + LlamaIndex**  | 永続ベクトルストアで巨大リポジトリも高速検索／RAG 拡張が容易     |
| **🔍 Git メタデータ連携**     | コミット履歴を取得し文脈に沿った提案を生成                       |
| **🚀 動的環境構築 run.sh**    | ビルド最小化・即時スクリプト反映・本番／開発切替に対応           |
| **♻️ 変更検知ウォッチャ**    | ファイル変更を自動検出しインデックスを部分再構築                 |
| **📜 .env + config.py**       | *すべての設定値は .env に統一し*、**`config.py` 経由でのみ参照** |
| **🪄 マルチプロジェクト拡張** | `.env.*` と複数 app サービスを並列にするだけで複数リポジトリ対応 |

---

## 🔭 将来的な構想

このスタックは以下の方向性で拡張を予定しています：

| 拡張項目             | 内容                                                                      |
| -------------------- | ------------------------------------------------------------------------- |
| LangChain Agent 導入 | `ReActAgent` や `ToolAgent` による対話的コード解析                        |
| Git 自動分析         | コミット履歴や blame 情報からバグ傾向・責任範囲を推論                     |
| Tool 呼び出し連携    | `flake8`, `mypy`, `gitleaks` など Linter/CLI を LangChain Tool 経由で実行 |
| コード提案・修正     | AI による修正提案（patch 生成）と Git 操作の自動化支援                    |
| 条件分岐型プロンプト | 複数 Tool を連携させるマルチステップ推論・状況判断処理                    |

これらは段階的に module 分離された形で追加予定です。Issue/Pull Request も歓迎します。

---

## 📂 ディレクトリ構成

```text
GAAI00/
├── app/                    # Python ロジック
│   ├── config.py          # .env 変数を一元解決
│   ├── *.py               # UI, indexer, git, watcher, prompts
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.sh
│
├── .env.example           # すべてのキーとデフォルトを提示
├── docker-compose.yml
├── chroma_data/           # ← 自動生成・Git 管理外
├── docs/
└── etc.
```

> **NOTE** : 旧 `utils.py` は **`config.py` に統合** されました。

---

## ⚙️ 環境変数一覧 (.env)

| 変数                | 役割                                              | 例                 | 旧版との差分         |
| ------------------- | ------------------------------------------------- | ------------------ | -------------------- |
| `CHROMA_HOST`       | Chroma サーバホスト (Docker 内)                   | chroma             | **New**              |
| `PORT_CHROMA`       | Chroma ポート                                     | 8000               | **New**              |
| `CHROMA_URL`        | 自動生成 (`http://${CHROMA_HOST}:${PORT_CHROMA}`) | –                  | –                    |
| `CHROMA_DATA_DIR`   | Chroma 永続データパス (Container)                 | /chroma-data       | **New**              |
| `CHROMA_COLLECTION` | コレクション名                                    | source-code        | ↗︎ 旧 README 未記載 |
| `PROJECT_PATH`      | ホスト側プロジェクトパス                          | /home/user/myproj  | same                 |
| `PROJECT_DIR`       | コンテナ内マウント先                              | /workspace/project | same                 |
| `OPENAI_API_KEY`    | LLM API キー                                      | sk-...             | same                 |
| `UI_MODE`           | `streamlit` / `gradio`                            | streamlit          | same                 |
| `PORT_STREAMLIT`    | 外部公開ポート                                    | 8501               | **New**              |
| `PORT_GRADIO`       | 外部公開ポート                                    | 7860               | **New**              |

### .env サンプル

```dotenv
# Chroma
CHROMA_HOST=chroma
PORT_CHROMA=8000
CHROMA_DATA_DIR=/chroma-data
CHROMA_COLLECTION=source-code

# Ports
PORT_STREAMLIT=8501
PORT_GRADIO=7860

# Project mount
PROJECT_PATH=/home/user/myproject
PROJECT_DIR=/workspace/project

# LLM
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# UI
UI_MODE=streamlit
```

> `.env.example` をコピーして編集してください。CI で欠損チェックが走ります。

---

## 🏗️ セットアップ

```bash
# 1. 環境変数を用意
cp .env.example .env
vi .env  # ← 必要箇所を変更

# 2. 起動
docker compose up --build
```

* **初回起動** : `PROJECT_PATH` 全体をインデックス
* **次回以降** : 変更差分のみを自動インデックス
* UI URL :

  * Streamlit → `http://localhost:${PORT_STREAMLIT}`
  * Gradio   → `http://localhost:${PORT_GRADIO}`

---

## 🔧 開発ヒント

* `run.sh` は *背景で `watcher.py` を起動* し、UI を選択起動します。
* 新規定数を追加する際は **必ず `.env.example` → `config.py`** の流れで統一。
* Python 依存 (一部更新)

  * `llama-index-embeddings-openai` ✅ *New*
  * `llama-index-readers-file` ✅ *New*
  * その他バージョンは `requirements.txt` を参照。

---

## 🤝 コントリビュート指針

1. `feature/xx` ブランチで開発し PR
2. **CI** (lint / syntax / Docker build) が緑になることを確認
3. `.env.example`・ドキュメント更新を忘れずに
4. Merge 後 `CHANGELOG.md` 更新 & タグ付与

---

## 参考リポジトリ & 文献

* [https://github.com/jerryjliu/llama\_index](https://github.com/jerryjliu/llama_index)
* [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
* [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)
* [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
* LangChain Cookbook: [https://docs.langchain.com/](https://docs.langchain.com/)
* LlamaIndex Guide: [https://docs.llamaindex.ai/](https://docs.llamaindex.ai/)

---

## 📄 ライセンス

MIT License – see [LICENSE](LICENSE)
