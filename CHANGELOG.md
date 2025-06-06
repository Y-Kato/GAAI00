# CHANGELOG

すべての主な変更・追加機能・修正履歴を記録します。
バージョニングは Semantic Versioning (例: MAJOR.MINOR.PATCH) に準拠します。

---

## [0.2.0] - 2025-06-06

### 🚀 大規模リファクタリング

**アーキテクチャの完全分離**
* **単一責任化**: UI層、ビジネスロジック層、インフラ層を完全分離
* **テスタビリティ向上**: `core_chat.answer()` 関数が retriever/llm をDI可能に
* **UI拡張性**: 新UIは `ChatSession` を呼ぶだけで追加可能

**新しいモジュール構成**
* `app_context.py`: グローバルなretriever/llm初期化
* `chat_session.py`: セッション管理層（履歴保持等）
* `core_chat.py`: ビジネスロジック（検索→プロンプト生成→LLM呼び出し）
* `ui_streamlit.py`: Streamlit UI専用モジュール
* `ui_gradio.py`: Gradio UI専用モジュール

**設定管理の改善**
* Pydantic Settings による型安全な設定管理
* `.env` からの自動読み込みと検証
* 設定プロパティの動的生成（`CHROMA_URL`等）

### 🔧 追加された機能

* **エラーハンドリング強化**: 各モジュールで適切な例外処理を追加
* **ログ出力改善**: 初期化プロセスの可視化とデバッグ情報充実
* **型安全性**: Pydantic による設定値の型検証

### 🔄 変更された点

* **config.py**: Pydantic Settingsベースに全面書き換え
* **main.py**: CLI エントリーポイントを簡素化
* **run.sh**: UI起動ロジックを Streamlit CLI 呼び出しに統一
* **requirements.txt**: `pydantic-settings>=2.0.0` を追加

### 🗑️ 削除・廃止

* `main_old.py`: 旧実装をアーカイブ化
* インラインのハードコーディング値を全廃
* 重複する LlamaIndex 設定コードを統合

### 💡 今後の拡張ポイント

* `core_chat` 各関数への pytest 導入準備完了
* LangChain Agent 化のためのDI（依存性注入）基盤完成
* retriever の search_kwargs .env変数化による柔軟なチューニング対応

### 🧪 CI/CD改善

* `.env.example` の完全性チェック強化
* Docker multi-stage build 最適化検討

### 📋 マイグレーション手順

1. 既存の `.env` ファイルを `.env.example` と比較し、新しい変数を追加
2. `docker compose build --no-cache` で依存関係を再構築
3. `docker compose up` で新アーキテクチャを起動

---

## [0.1.0] - 2025-05-30

### 初期リリース

* LlamaIndex + LangChain によるコードインデックス＆リファクタ提案基盤を構築
* Streamlit / Gradio によるチャット型UIを実装
* Chroma による永続ベクトルストア接続
* Git 履歴を用いたメタデータ抽出機能を追加
* Watchdog による変更監視とインクリメンタルインデックス更新機能を統合
* Docker Compose による完全コンテナ化構成
* `.env.example` による柔軟なプロジェクト指定に対応

### メンテナンス

* `.gitignore`、`.dockerignore` を整備
* MIT ライセンスを追加

### CI/CD

* GitHub Actions による CI ワークフローを導入（`.github/workflows/main.yml`）
  * Python構文チェック（compileall）
  * Docker Compose のビルド確認
* `README.md` に CIバッジ、Last Commitバッジ、Licenseバッジを追加

---

**次期バージョン予定**:
- [x] アーキテクチャ分離 (v0.2.0)
- [ ] LangChain Agent 機能 (v0.3.0)
- [ ] マルチプロジェクト対応 (v0.4.0)
- [ ] DockerHub連携 (v1.0.0)