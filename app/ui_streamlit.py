import streamlit as st
from chat_session import ChatSession
from app_context import retriever, llm

_session = ChatSession(retriever, llm)

def launch():
    st.title("🦙🔗 LlamaIndex × LangChain Dev Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # replay history
    for m in st.session_state.messages:
        st.markdown(m)

    if prompt := st.chat_input("コードを貼り付けて質問…"):
        st.session_state.messages.append(f"**🧑‍💻:** {prompt}")
        with st.spinner("thinking…"):
            resp = _session.respond(prompt)
        st.session_state.messages.append(f"**🤖:** {resp}")
        st.experimental_rerun()

if __name__ == "__main__":
    launch()