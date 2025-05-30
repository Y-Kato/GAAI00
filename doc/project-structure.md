# GAAI00 開発支援スタック：リポジトリ設計方針

## ディレクトリ構成の方針

```
GAAI00/
├── app/                     # 全アプリケーションロジック（Python）
│   ├── *.py                 # 各種モジュール：UI, indexer, git, etc.
│   ├── requirements.txt     # Python依存
│   ├── Dockerfile
│   └── run.sh
│
├── .github/workflows
│   └── main.yml             # CI
│
├── chroma_data/             # Chroma のベクトルストア（Docker Volume）→ .gitignore
├── .env.example             # サンプル環境設定（← .env は無視）
├── docker-compose.yml
├── README.md
├── LICENSE
├── .dockerignore
├── .gitignore
└── docs/                    # 任意：設計図、構成図、チュートリアル
```

---

## Git管理ポリシー

### Gitに含めるべきファイル

* `.env.example`
* `app/*.py`, `Dockerfile`, `run.sh`, `requirements.txt`
* `README.md`, `LICENSE`, `.gitignore`, `.dockerignore`
* `docker-compose.yml`

### Gitに含めない（`.gitignore`登録）

```
# 環境情報
.env
*.env

# Python キャッシュ
__pycache__/
*.py[cod]

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/

# Git ロード
.git/
.gitignore
.github/ISSUE_TEMPLATE/

# Docker 実行データ
chroma_data/
app/.last_indexed_commit
```

---

## 運用フロー

### ローカル開発

* `.env` でローカルプロジェクトをマウント
* `docker compose up --build` で簡単起動
* Gitと連携して更新を自動検知

### リリース（メモ・案）

* `main` へのマージ時に `v0.x.x` タグ付与
* `CHANGELOG.md` に詳細書く

### コントリビュート方針（メモ・案）

* `feature/xxx` や `fix/xxx` ブランチ
* PR時は、Dockerで実行確認必須
* LLM関係ならスクショも添付

---

## docs/ 構成案

| ファイル                 | 内容                      |
| -------------------- | ----------------------- |
| `architecture.md`    | 構成図 & モジュール分析           |
| `usage.md`           | .env設定やチュートリアル          |
| `extend.md`          | LangChain Agent などの拡張方法 |
| `troubleshooting.md` | よくあるエラー対処               |

---

## バージョン管理戦略（メモ・案）

* `v0.1.0` 最小構成コンプリート
* `v0.2.0` LangChain Agent 対応
* `v1.0.0` 穩定分岐

---

## 拡張性を前提とした設計（メモ・案）

| 拡張要素         | 現状               | 拡張例                            |
| ------------ | ---------------- | ------------------------------ |
| Vector Store | Chroma           | Qdrant, FAISS, Weaviate など     |
| LLM          | OpenAI固定         | HuggingFace, Local(LLaMA.cpp等) |
| Prompt定義     | Python内に固定       | YAMLまたはUIで編集可能に                |
| UI           | Gradio/Streamlit | Next.js, REST APIへ分離構成         |
| 自動評価・ログ      | 未導入              | LangSmith や GitHub Actions 連携  |


