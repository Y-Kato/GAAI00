"""Gradio / Streamlit unified chat UI."""
import argparse
import asyncio
from pathlib import Path
from typing import List

import gradio as gr
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from config import PROJECT_DIR, INDEXED_FLAG_FILE
from indexer import build_full_index, incremental_update
from git_metadata import commit_messages
from prompts import REFRACTOR_PROMPT

# One‑time full index if needed
if not Path(INDEXED_FLAG_FILE).exists():
    build_full_index()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)


def answer(query: str):
    incremental_update()
    # For demo, we just call the LLM with prompt; retrieval can be added
    history_text = "\n".join(f"* {c['message']} ({c['author']}, {c['date']})" for c in commit_messages(5))
    prompt = REFRACTOR_PROMPT.format(code=query, history=history_text)
    resp = llm([HumanMessage(content=prompt)])
    return resp.content


def _gradio():
    with gr.Blocks() as demo:
        gr.Markdown("## 📐 コードリファクタ チャット")
        chat = gr.Chatbot()
        inp = gr.Textbox(label="コードまたは質問を入力…")

        def respond(message, history):
            return answer(message)

        inp.submit(respond, [inp, chat], chat)

    demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False)


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