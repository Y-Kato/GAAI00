# LlamaIndex + LangChain Dev Assistant Stack (Docker-Compose)

このリポジトリは、LlamaIndex と LangChain を活用しソースコードベースの**開発支援・保守支援**を目的とした Docker 構成です。
Gradio/StreamlitベースのチャットUIを通じて、コードのリファクタ提案、Git履歴に基づくメタ情報の付与、変更の自動検出と再インデックスなど、開発に役立つ基本的な機能が統合された素体として構成されています。

---

## 特徴

・ **LlamaIndex + LangChain** による自然言語対話型のコードリファクタ提案
・ **Git履歴を活用したメタデータ付与**
・ **ソース変更の自動検知 & 増分インデックス更新**
・ **Chroma による永続ベクトルストア構成**
・ **Gradio / Streamlit UI（選択可能）**
・ **完全Docker化** により、簡単かつ再現可能な開発環境構築

---

## ディレクトリ構成

```
project-root/
├─ docker-compose.yml
├─ .env.example              ← 環境に合わせて編集
├─ app/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ run.sh
│  ├─ main.py
│  ├─ indexer.py
│  ├─ git_metadata.py
│  ├─ watcher.py
│  ├─ prompts.py
│  └─ utils.py
└─ chroma_data/              ← 自動生成される永続ボリューム領域
```

---

## セットアップ方法

### 1. `.env` ファイルの準備

```bash
cp .env.example .env
```

環境に合わせて編集：

```dotenv
PROJECT_PATH=/path/to/your/project    # 自分のソースコードの符合パスに変更
PROJECT_DIR=/workspace/project        # Dockerコンテナ内部でプロジェクトがマウントされるパス
OPENAI_API_KEY=sk-***your-api-key***  # OpenAI API キーをここに記入（公開前に削除）
UI_MODE=streamlit                     # または gradio
```

### 2. Dockerビルドと起動

```bash
docker compose up --build
```

起動後、以下のURLからアクセス：

* Streamlit: [http://localhost:8501](http://localhost:8501)
* Gradio: [http://localhost:7860](http://localhost:7860)

---

## 初回実行時の動作

初回起動時に、指定された`PROJECT_PATH`内のすべてのファイルを全文インデックス化します。
以降は、ファイル変更やGitコミットに応じて自動的に差分のみを再インデックスします。

---

## チャットでできること

* ソースコードを貼り付けて改善点を問うと、LLMが **日本語で明確なリファクタ提案**を返します。
* Git履歴も参照するため、**文脈に正しい提案**が可能です。

---

## 開発者向けメモ

* `llama-index-core==0.10.39`
* `langchain==0.1.14` + `langchain-community==0.0.30` ← 必須
* `chromadb[server]==0.4.24` を使用（永続型ベクトルストア）

---

## 公開前に確認すべきこと

* `.env`に含まれる**APIキーやローカルパス**は必ず削除またはマスクしてください。
* `project-root/app`下に**プロジェクト固有の情報**が添われていないか再確認してください。

---

##  貢献・汎用プロジェクト

この構成は拡張性があります。たとえば以下のような改良が可能です：

* Retrieval-Augmented Generation (RAG)の導入
* LangChain Agent による対話指向の改善
* VSCode Remote Container への統合

---

## 参考リポジトリ & 文献

* [https://github.com/jerryjliu/llama\_index](https://github.com/jerryjliu/llama_index)
* [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
* [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)
* [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
* LangChain Cookbook: [https://docs.langchain.com/](https://docs.langchain.com/)
* LlamaIndex Guide: [https://docs.llamaindex.ai/](https://docs.llamaindex.ai/)

---

## ライセンス

[MIT License](LICENSE)
