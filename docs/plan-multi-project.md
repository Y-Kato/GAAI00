# LlamaIndex 複数プロジェクト対応計画

本ドキュメントは、LlamaIndex + LangChain スタックにおける複数プロジェクト対応方法の比較、および将来的な拡張方針（サービス分離案）を記録したものである。

> **目的** : Chroma インスタンスは 1 つに保ちながら、複数のコードベースを独立して扱い、それぞれのインデックスを分離すること。

---

## 検討された3方式の要約

| 方法 | 概要 | 長所 | 短所 | 対応レベル |
|------|------|------|------|------------|
| **① 統合一括読込** | 複数ディレクトリを `SimpleDirectoryReader(input_dirs=[...])` で読み込み、単一の Chroma コレクションへ統合 | 実装が最もシンプル | プロジェクト境界が曖昧になりやすい | PoC・簡易用途向け |
| **② サービス分離型** | 各プロジェクトごとに Chroma コレクションおよびインデクサ/UI を完全に分離し、複数 Compose サービスを持つ | プロジェクト単位で完全独立可能。Git履歴や再構築も安全 | リソース使用量増加、UI切り替えが手動 | 🔜 **本構成では今後これを採用予定** |
| **③ メタデータタグ分離型** | 同一コレクションに複数ソースを統合しつつ、各 `Document.metadata["project"]` により識別可能に | 検索・チャットUIにおいて柔軟なフィルター処理が可能 | 実装が若干複雑、データ量増に注意 | サービス連携・UI統合型向け |

---

## 今後の拡張方針（方式②）

以下の構成でプロジェクトごとの完全分離を実現する：

- 各プロジェクト = 独立した `llc-app` サービス名と `.env` 設定を持つ
- 例：
  - `llc-app-proj1`（`PROJECT_PATH=/host/repo1`, `CHROMA_COLLECTION=repo1`, port 8501）
  - `llc-app-proj2`（`PROJECT_PATH=/host/repo2`, `CHROMA_COLLECTION=repo2`, port 8502）
- `docker-compose.yml` で複数 app サービスを並列管理

---

## 1 ディレクトリ構成

```
GAAI00/
├── compose.yml
├── envs/
│   ├── .env.projectA
│   └── .env.projectB
└── etc.
```

* `envs/` はプロジェクトごとの変数差分（コレクション名、ポート、パスなど）を格納。
* **ルール** : 差分が必要な変数だけを定義し、共通値は `.env.example` に記載。

---

## 2 docker-compose の拡張例

```yaml
# compose.yml（ルート）
services:
  chroma:
    image: chromadb/chroma:0.5
    restart: unless-stopped
    volumes:
      - ./chroma_data:/chroma-data
    ports:
      - "8000:8000"

  app_projectA:
    env_file: envs/.env.projectA
    build: ./app
    depends_on: [chroma]
    ports:
      - "8501:8501"   # PORT_STREAMLIT を projectA 用に上書き

  app_projectB:
    env_file: envs/.env.projectB
    build: ./app
    depends_on: [chroma]
    ports:
      - "8502:8501"   # ホスト側ポートのみリマップ
```

---

## 3 `.env.projectA` のサンプル

```dotenv
# Chroma（共通）
CHROMA_COLLECTION=projectA-code

# UI ポート
PORT_STREAMLIT=8501
PORT_GRADIO=7861

# 対象リポジトリ
PROJECT_PATH=/home/user/projectA
```

`.env.projectB` では `CHROMA_COLLECTION`, `PORT_STREAMLIT`, `PROJECT_PATH` を変更する。

---

## 4 ルーティングに関するヒント

| ユースケース   | 推奨構成例                                          |
| -------- | ---------------------------------------------- |
| リバースプロキシ | Traefik / Caddy + サービス別ラベル                     |
| HTTPS 対応 | Let's Encrypt のワイルドカード証明書 + DNS 経由で解決          |
| メモリ制限    | `mem_limit: 4g` を compose.yml 内で app サービスごとに指定 |

---

## 5 CI におけるマトリクス戦略

GitHub Actions の `strategy.matrix.env-file` を使って、各 `.env.*` に対応した統合テストを並列実行する。
