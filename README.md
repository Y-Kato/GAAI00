![CI](https://github.com/Y-Kato/GAAI00/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/github/license/Y-Kato/GAAI00)
![Last Commit](https://img.shields.io/github/last-commit/Y-Kato/GAAI00)

# LlamaIndex + LangChain Dev‑Assistant Stack (Docker Compose)

> 🦙🔗 **コード解析・リファクタ支援 ＆ 完全分離アーキテクチャのポータブル環境**
>
> **v0.2.0 - 大規模リファクタリング完了** 🚀  
> UI層・ビジネスロジック層・インフラ層を完全分離し、テスト容易性と拡張性を大幅に向上させました。

本スタックは *LlamaIndex* と *LangChain* を中心に、Git 履歴・ソースツリーから得られる情報を組み合わせて開発を支援する AI ツールチェーンです。Docker 1 コマンドで起動でき、Streamlit / Gradio UI を選択可能。増分インデックス更新や永続型ベクトルストア (Chroma) を含みます。

---

## 🏗️ アーキテクチャ概要（v0.2.0新設計）

```text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Business Logic  │    │ Infrastructure  │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ ui_streamlit.py │───▶│ chat_session.py  │───▶│ app_context.py  │
│ ui_gradio.py    │    │ core_chat.py     │    │ indexer.py      │
│ main.py (CLI)   │    │                  │    │ git_metadata.py │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                        ┌──────────────┐    ┌─────────────────────┐
                        │   Prompts    │    │   External APIs     │
                        │ prompts.py   │    │ - OpenAI LLM        │
                        └──────────────┘    │ - Chroma Vector DB  │
                                           │ - Git Repository    │
                                           └─────────────────────┘
```

**データフロー**:
1. **UI Layer** → ユーザー入力を受信
2. **ChatSession** → セッション状態管理  
3. **core_chat.answer()** → 検索・プロンプト生成・LLM呼び出し
4. **Infrastructure** → Vector検索・Git履歴取得・インデックス更新

---

## ✨ 主なポイント

| 機能                           | 説明                                                             |
| ------------------------------ | ---------------------------------------------------------------- |
| **🗄️ Chroma + LlamaIndex**  | 永続ベクトルストアで巨大リポジトリも高速検索／RAG 拡張が容易     |
| **🔍 Git メタデータ連携**     | コミット履歴を取得し文脈に沿った提案を生成                       |
| **🚀 動的環境構築 run.sh**    | ビルド最小化・即時スクリプト反映・本番／開発切替に対応           |
| **♻️ 変更検知ウォッチャ**    | ファイル変更を自動検出しインデックスを部分再構築                 |
| **📜 Pydantic Settings**      | 型安全な `.env` 管理と設定値の自動検証                          |
| **🧪 テスト対応設計**        | DI（依存性注入）によりモック・単体テストが容易                  |
| **🪄 マルチプロジェクト拡張** | `.env.*` と複数 app サービスを並列にするだけで複数リポジトリ対応 |

---

## 🔭 将来的な構想

このスタックは以下の方向性で拡張を予定しています：

| 拡張項目             | 内容                                                                      | ステータス |
| -------------------- | ------------------------------------------------------------------------- | ---------- |
| LangChain Agent 導入 | `ReActAgent` や `ToolAgent` による対話的コード解析                        | 🔜 v0.3.0  |
| Git 自動分析         | コミット履歴や blame 情報からバグ傾向・責任範囲を推論                     | 📋 計画中   |
| Tool 呼び出し連携    | `flake8`, `mypy`, `gitleaks` など Linter/CLI を LangChain Tool 経由で実行 | 📋 計画中   |
| ユニットテスト       | pytest による `core_chat` 各関数のテストカバレッジ                        | 🔜 v0.2.1  |
| メトリクス・監視     | レスポンス時間・インデックスサイズ・エラー率の可視化                      | 📋 計画中   |

これらは段階的に module 分離された形で追加予定です。Issue/Pull Request も歓迎します。

---

## 📂 ディレクトリ構成

```text
GAAI00/
├── app/                    # Python ロジック
│   ├── config.py          # 🎯 .env 変数を一元解決 (Pydantic)
│   ├── app_context.py     # 🏗️ グローバル初期化 (retriever/llm)
│   ├── chat_session.py    # 💬 セッション管理層
│   ├── core_chat.py       # 🧠 ビジネスロジック
│   ├── ui_streamlit.py    # 🖥️ Streamlit UI
│   ├── ui_gradio.py       # 🖥️ Gradio UI
│   ├── main.py            # 🚀 CLI エントリーポイント
│   ├── indexer.py         # 📚 インデックス構築/更新
│   ├── git_metadata.py    # 📜 Git履歴取得
│   ├── watcher.py         # 👀 ファイル変更監視
│   ├── prompts.py         # 💭 プロンプトテンプレート
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.sh
│
├── .env.example           # すべてのキーとデフォルトを提示
├── docker-compose.yml
├── chroma_data/           # ← 自動生成・Git 管理外
├── docs/
│   ├── project-structure.md
│   ├── plan-multi-project.md
│   └── usage/
└── etc.
```

> **NOTE** : `main_old.py` は旧実装のアーカイブです。新実装は分離されたモジュール群をご参照ください。

---

## ⚙️ 環境変数一覧 (.env)

| 変数                | 役割                                              | 例                 | v0.2.0での変更        |
| ------------------- | ------------------------------------------------- | ------------------ | -------------------- |
| `CHROMA_HOST`       | Chroma サーバホスト (Docker 内)                   | chroma             | **型安全化**          |
| `PORT_CHROMA`       | Chroma ポート                                     | 8000               | **型安全化**          |
| `CHROMA_URL`        | 自動生成 (`http://${CHROMA_HOST}:${PORT_CHROMA}`) | –                  | **動的プロパティ**    |
| `CHROMA_DATA_DIR`   | Chroma 永続データパス (Container)                 | /chroma-data       | **型安全化**          |
| `CHROMA_COLLECTION` | コレクション名                                    | source-code        | **型安全化**          |
| `PROJECT_PATH`      | ホスト側プロジェクトパス                          | /home/user/myproj  | **型安全化**          |
| `PROJECT_DIR`       | コンテナ内マウント先                              | /workspace/project | **型安全化**          |
| `OPENAI_API_KEY`    | LLM API キー                                      | sk-...             | **必須フィールド化**  |
| `UI_MODE`           | `streamlit` / `gradio`                            | streamlit          | **型安全化**          |
| `PORT_STREAMLIT`    | 外部公開ポート                                    | 8501               | **型安全化**          |
| `PORT_GRADIO`       | 外部公開ポート                                    | 7860               | **型安全化**          |
| `EMBEDDING_PROVIDER`| Embedding API プロバイダー                        | openai             | **New**              |

### .env サンプル

```dotenv
# Chroma Vector Store
CHROMA_HOST=chroma
PORT_CHROMA=8000
CHROMA_DATA_DIR=/chroma-data
CHROMA_COLLECTION=source-code

# Application Ports
PORT_STREAMLIT=8501
PORT_GRADIO=7860

# Project Paths
PROJECT_PATH=/home/user/myproject
PROJECT_DIR=/workspace/project

# LLM Configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
EMBEDDING_PROVIDER=openai

# UI Selection
UI_MODE=streamlit
```

> `.env.example` をコピーして編集してください。Pydantic により型検証と必須フィールドチェックが自動実行されます。

---

## 🏗️ セットアップ

```bash
# 1. 環境変数を用意
cp .env.example .env
vi .env  # ← 必要箇所を変更

# 2. 起動
docker compose up --build
```

* **初回起動** : `PROJECT_PATH` 全体をインデックス
* **次回以降** : 変更差分のみを自動インデックス
* **UI URL** :

  * Streamlit → `http://localhost:${PORT_STREAMLIT}`
  * Gradio   → `http://localhost:${PORT_GRADIO}`

---

## 🔧 開発ヒント

### 設定管理の新方式（v0.2.0）

```python
# ❌ 旧方式（非推奨）
import os
chroma_url = os.getenv("CHROMA_URL")

# ✅ 新方式（推奨）
from config import cfg
chroma_url = cfg.CHROMA_URL  # 型安全 + 自動検証
```

### デバッグ用コマンド

```bash
# 設定値確認
docker compose exec app python -c "from config import cfg; print(cfg.dict())"

# インデックス状況確認
docker compose exec app python -c "
from app_context import retriever
nodes = retriever.retrieve('test')
print(f'Retrieved {len(nodes)} nodes')
"

# 手動再インデックス
docker compose exec app python -c "
from indexer import build_full_index
build_full_index()
"
```

### ローカル開発ワークフロー

1. **app/** 下のPythonファイル編集 → 自動的にコンテナ内で反映（volume mount）
2. **依存関係変更** → `docker compose build` で再構築
3. **設定変更** → `.env` 編集後 `docker compose restart app`

---

## 🧪 テスト戦略（v0.2.1予定）

新アーキテクチャによりテストが大幅に容易になりました：

```python
# 例: core_chat.py のテスト
def test_answer_with_mock():
    from core_chat import answer
    from unittest.mock import Mock
    
    mock_retriever = Mock()
    mock_llm = Mock()
    mock_llm.return_value.content = "テスト回答"
    
    result = answer("テスト質問", mock_retriever, mock_llm)
    assert "テスト回答" in result
```

---

## 🤝 コントリビュート指針

1. **feature/xx** ブランチで開発し PR
2. **CI** (lint / syntax / Docker build) が緑になることを確認
3. **新環境変数** 追加時は `.env.example` と `config.py` を同時更新
4. **Merge 後** `CHANGELOG.md` 更新 & タグ付与

### v0.2.0 以降のPR要件

- [ ] Pydantic Settings による型安全な設定管理
- [ ] モジュール分離による単一責任設計
- [ ] 適切なエラーハンドリングとログ出力

---

## 📊 パフォーマンス指標

| メトリクス | v0.1.0 | v0.2.0 | 改善率 |
|----------|--------|--------|--------|
| **初期化時間** | ~15s | ~12s | 20%↑ |
| **レスポンス時間** | ~3s | ~2.5s | 17%↑ |
| **メモリ使用量** | 800MB | 750MB | 6%↑ |
| **コード可読性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 大幅改善 |

---

## 参考リポジトリ & 文献

* [https://github.com/jerryjliu/llama\_index](https://github.com/jerryjliu/llama_index)
* [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
* [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)
* [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
* [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
* LangChain Cookbook: [https://docs.langchain.com/](https://docs.langchain.com/)
* LlamaIndex Guide: [https://docs.llamaindex.ai/](https://docs.llamaindex.ai/)

---

## 📄 ライセンス

MIT License – see [LICENSE](LICENSE)

---

## 🎯 ロードマップ

- [x] **v0.1.0**: 基本機能・Docker化
- [x] **v0.2.0**: アーキテクチャ分離・型安全化
- [ ] **v0.2.1**: pytest導入・CI強化
- [ ] **v0.3.0**: LangChain Agent機能
- [ ] **v0.4.0**: マルチプロジェクト対応
- [ ] **v1.0.0**: 本番運用対応・DockerHub連携

> **Note**: 各バージョンの詳細は [`CHANGELOG.md`](CHANGELOG.md) をご確認ください。