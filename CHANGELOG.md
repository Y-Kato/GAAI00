# CHANGELOG

すべての主な変更・追加機能・修正履歴を記録します。
バージョニングは Semantic Versioning (例: MAJOR.MINOR.PATCH) に準拠します。

---

## \[0.2.0] – 2025-06-05

### 追加された機能

* `.env` を中心とした完全な設定管理構成に移行し、`config.py` に集約。
* 新規環境変数の追加：`CHROMA_HOST`, `PORT_CHROMA`, `CHROMA_DATA_DIR`, `CHROMA_COLLECTION`, `PORT_STREAMLIT`, `PORT_GRADIO`, `UI_MODE`, `EMBEDDING_PROVIDER`。
* `watcher.py` によるインクリメンタルなインデックス更新機構を追加。
* UI 切り替え（Streamlit / Gradio）を `.env` 経由で動的選択可能に。
* README / usage / project-structure / plan-multi-project などドキュメントを全面刷新。

### 変更された点

* 旧 `utils.py` を廃止し、**Pydantic ベースの `config.py`** に移行。
* Docker ビルド構成を簡素化し、実行スクリプトを `run.sh` に集約。

### 削除された点

* ハードコードされたパスや環境依存処理。

### マイグレーション手順

1. 新しい `.env.example` を参照し、既存 `.env` を置き換えまたは統合してください。
2. アップグレード後は `docker compose build --no-cache` を推奨。
3. CI での `.env.ci` に `PORT_STREAMLIT`, `PORT_GRADIO` を追加してください。

---

## \[0.1.0] - 2025-05-30

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

次のバージョンでは、DockerHub連携を検討中
