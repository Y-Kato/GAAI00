import argparse
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
import gradio as gr

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import HttpClient

from config import cfg
from indexer import build_full_index, incremental_update
from git_metadata import commit_messages
from prompts import REFRACTOR_PROMPT

# ----------------------------
# 初期セットアップ
# ----------------------------
if not Path(cfg.INDEXED_FLAG_FILE).exists():
    build_full_index()

# LangChain LLM を設定
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# ベクトルストア接続
url = urlparse(cfg.CHROMA_URL)
chroma_client = HttpClient(host=url.hostname, port=url.port)
collection = chroma_client.get_or_create_collection(name=cfg.CHROMA_COLLECTION)

vector_store = ChromaVectorStore(
    chroma_collection=collection,
    collection_name=cfg.CHROMA_COLLECTION,
    persist_dir=str(cfg.CHROMA_PERSIST_DIR),
    host=url.hostname,
    port=url.port,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Retriever 構築（LLM は使わない）
index = VectorStoreIndex.from_vector_store(vector_store)
retriever = index.as_retriever(search_kwargs={"k": 6})

# ----------------------------
# 回答生成
# ----------------------------
def answer(query: str) -> str:
    try:
        incremental_update()
    except Exception as e:
        print(f"[MAIN][ERROR] incremental_update() failed: {e}")

    try:
        nodes = retriever.retrieve(query)
        retrieved_text = "\n\n".join(n.get_content() for n in nodes)

        history_text = "\n".join(
            f"* {c['message']} ({c['author']}, {c['date']})"
            for c in commit_messages(5)
        )

        full_prompt = REFRACTOR_PROMPT.format(
            code=retrieved_text,
            history=history_text
        )
        resp = llm([HumanMessage(content=full_prompt)])
        return resp.content

    except Exception as e:
        print(f"[MAIN][ERROR] LLM call failed: {e}")
        return "❌ 内部エラーが発生しました。ログをご確認ください。"

# ----------------------------
# UI: Gradio
# ----------------------------
def _gradio():
    with gr.Blocks() as demo:
        gr.Markdown("## 📐 コードリファクタ チャット")
        chat = gr.Chatbot()
        inp = gr.Textbox(label="コードまたは質問を入力…")

        def respond(message, history):
            return answer(message)

        inp.submit(respond, [inp, chat], chat)

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=cfg.PORT_GRADIO,
        share=False
    )

# ----------------------------
# UI: Streamlit
# ----------------------------
def _streamlit():
    st.title("🦙🔗 LlamaIndex LangChain Dev Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        st.markdown(m)

    if prompt := st.chat_input("コードを貼り付けて質問…"):
        st.session_state.messages.append(f"**🧑‍💻:** {prompt}")
        with st.spinner("thinking…"):
            resp = answer(prompt)
        st.session_state.messages.append(f"**🤖:** {resp}")
        st.experimental_rerun()

# ----------------------------
# Entry Point
# ----------------------------
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", choices=["gradio", "streamlit"], default="streamlit")
    args = parser.parse_args()
    if args.ui == "gradio":
        _gradio()
    else:
        _streamlit()

if __name__ == "__main__":
    cli()
