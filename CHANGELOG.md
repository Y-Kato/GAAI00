# CHANGELOG

すべての主な変更・追加機能・修正履歴を記録します。
バージョニングは Semantic Versioning (例: MAJOR.MINOR.PATCH) に準拠します。

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
