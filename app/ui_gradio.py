import gradio as gr
from chat_session import ChatSession
from app_context import retriever, llm
from config import cfg    # ★追加

_session = ChatSession(retriever, llm)

def launch():
    with gr.Blocks() as demo:
        gr.Markdown("## 📐 コードリファクタ チャット")
        chat = gr.Chatbot()
        inp = gr.Textbox(label="コードまたは質問を入力…")

        def respond(message, history):
            return _session.respond(message)

        inp.submit(respond, [inp, chat], chat)

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=cfg.PORT_GRADIO,   # ← .env の値を使用
        share=False
    )
