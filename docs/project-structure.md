# Project Structure & Design Conventions

> **v0.2.0 - 完全分離アーキテクチャ**  
> すべての設定は `.env → config.py` の流れで統一。ハードコードは禁止。

```
GAAI00/
├── app/
│   ├── config.py           # 🎯 中央設定管理 (Pydantic Settings)
│   ├── app_context.py      # 🏗️ グローバル初期化 (retriever/llm)
│   ├── chat_session.py     # 💬 セッション管理層
│   ├── core_chat.py        # 🧠 ビジネスロジック (検索→LLM)
│   ├── ui_streamlit.py     # 🖥️ Streamlit UI
│   ├── ui_gradio.py        # 🖥️ Gradio UI
│   ├── main.py             # 🚀 CLI エントリーポイント
│   ├── indexer.py          # 📚 Chroma インデックス構築/更新
│   ├── watcher.py          # 👀 ファイル変更監視
│   ├── git_metadata.py     # 📜 Git 履歴取得
│   ├── prompts.py          # 💭 LLM プロンプトテンプレート
│   ├── main_old.py         # 📦 旧実装アーカイブ
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.sh              # 🏃 起動スクリプト
│
├── docker-compose.yml      # 🐳 シングルノード構成 (app + chroma)
├── .env.example            # 📋 **全環境変数の正規リスト**
├── chroma_data/            # 💾 Chroma 永続化 (Git管理外)
├── docs/                   # 📚 ドキュメント
│   ├── project-structure.md
│   ├── plan-multi-project.md
│   └── usage/
├── .github/workflows/
└── etc/
```

---

## 🏗️ アーキテクチャ層分離

### データフロー図

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

### 責任分担

| レイヤー | モジュール | 責任 |
|---------|-----------|------|
| **UI** | `ui_*.py`, `main.py` | ユーザー入力処理、表示ロジック |
| **Business** | `chat_session.py`, `core_chat.py` | セッション管理、検索・LLM呼び出し |
| **Infrastructure** | `app_context.py`, `indexer.py` | 外部API接続、データ永続化 |
| **Config** | `config.py` | 環境変数管理、設定検証 |

---

## 🔧 必須規約

### 1. 設定管理ルール

```python
# ❌ 禁止: 直接的な os.getenv()
import os
db_url = os.getenv("CHROMA_URL")

# ✅ 推奨: config.py 経由
from config import cfg
db_url = cfg.CHROMA_URL
```

### 2. 新環境変数追加フロー

1. **`.env.example`** に変数とデフォルト値を追加
2. **`config.py`** の `Settings` クラスにフィールド追加
3. **CI** で必須キー検証が自動実行される

### 3. テスト可能設計

```python
# core_chat.py - DI対応で単体テスト可能
def answer(query: str, retriever, llm) -> str:
    # モック可能な引数として受け取る
    pass

# 使用例
from app_context import retriever, llm
result = answer("質問", retriever, llm)
```

---

## 📊 config.py 設計パターン

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 型安全＋デフォルト値
    CHROMA_HOST: str = "chroma"
    PORT_CHROMA: int = 8000
    OPENAI_API_KEY: str  # 必須フィールド
    
    class Config:
        env_file = ".env"
    
    @property
    def CHROMA_URL(self) -> str:
        # 動的プロパティ生成
        return f"http://{self.CHROMA_HOST}:{self.PORT_CHROMA}"

cfg = Settings()  # グローバルインスタンス
```

**利点**:
- 型安全性（IDE補完＋ランタイム検証）
- 一元管理（単一インポートで全設定にアクセス）
- テスト容易性（設定の上書きが簡単）

---

## 🔄 Git運用ポリシー

### ブランチ戦略

* **feature/\<name>** → PR → main
* **hotfix/\<bug>** → 緊急修正用
* **refactor/\<module>** → アーキテクチャ改善用

### PR要件

| チェック項目 | 必須 | 内容 |
|-------------|------|------|
| **CI通過** | ✅ | syntax check + Docker build |
| **`.env.example`更新** | ⚠️ | 新環境変数追加時 |
| **CHANGELOG.md** | ⚠️ | 機能追加・破壊的変更時 |
| **型安全性** | ✅ | mypy準拠（将来対応） |

### コミットメッセージ規約

```
feat: add LangChain Agent support
fix: resolve Chroma connection timeout
docs: update API documentation
refactor: separate UI and business logic
test: add unit tests for core_chat module
```

---

## 🧪 テスト戦略

### 単体テスト例

```python
# tests/test_core_chat.py
import pytest
from unittest.mock import Mock
from core_chat import answer, retrieve_code, generate_prompt

def test_retrieve_code():
    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = [Mock(get_content=lambda: "test code")]
    
    result = retrieve_code("test query", mock_retriever)
    assert "test code" in result

def test_answer_integration():
    mock_retriever = Mock()
    mock_llm = Mock()
    mock_llm.return_value.content = "リファクタ提案"
    
    result = answer("refactor this", mock_retriever, mock_llm)
    assert isinstance(result, str)
    assert "リファクタ提案" in result
```

### CI統合

```yaml
# .github/workflows/main.yml への追加
- name: Run unit tests
  run: |
    cd app
    python -m pytest tests/ -v --cov=.
```

---

## 🚀 パフォーマンス考慮事項

### 最適化目標

| コンポーネント | 最適化手法 | 効果 | ステータス |
|---------------|-----------|------|----------|
| **Chroma接続** | コネクションプール | レスポンス -30% | 🔜 v0.3.0 |
| **LLM呼び出し** | ストリーミング | 体感速度向上 | 📋 計画中 |
| **インデックス** | 増分更新 | ディスク削減 | ✅ 実装済み |

### Docker最適化

```dockerfile
# 将来のマルチステージビルド案
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
```

---

## 📈 拡張ロードマップ

### Phase 1: 安定性向上 (v0.2.x)

- [ ] pytest導入 + CI統合
- [ ] エラーハンドリング強化
- [ ] ログレベル設定可能化

### Phase 2: 機能拡張 (v0.3.x)

- [ ] LangChain Agent対応
- [ ] カスタムプロンプトテンプレート
- [ ] Tool呼び出し連携

### Phase 3: スケーラビリティ (v0.4.x)

- [ ] マルチプロジェクト対応
- [ ] 分散Chroma構成
- [ ] メトリクス・監視機能

---

## 🛠️ 開発者向けユーティリティ

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

# 手動インデックス再構築
docker compose exec app python -c "
from indexer import build_full_index
build_full_index()
"
```

### ローカル開発ワークフロー

1. **環境準備**: `cp .env.example .env` → 設定編集
2. **開発サーバー起動**: `docker compose up --build`
3. **コード変更**: app/ 下のファイル編集 → 自動反映
4. **デバッグ**: `docker compose logs app -f`

---

## 📚 参考資料

### 公式ドキュメント

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### 設計思想

- **Clean Architecture**: レイヤー分離による保守性向上
- **Dependency Injection**: テスタビリティとモック容易性
- **Configuration as Code**: `.env`中心の環境管理
- **Single Responsibility**: 各モジュールの責任明確化

---

## 🔗 関連ファイル

- [`docs/usage/`](./usage/) - 使用方法とセットアップガイド
- [`docs/plan-multi-project.md`](./plan-multi-project.md) - 複数プロジェクト対応計画
- [`.env.example`](../.env.example) - 環境変数テンプレート
- [`CHANGELOG.md`](../CHANGELOG.md) - 変更履歴

---

> **Note**: 本ドキュメントは v0.2.0 リファクタリング完了時点での構造を反映しています。将来のバージョンで構造が変更される可能性があります。最新情報は [`CHANGELOG.md`](../CHANGELOG.md) をご確認ください。