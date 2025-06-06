from langchain.schema import HumanMessage
from prompts import REFRACTOR_PROMPT
from git_metadata import commit_messages
from indexer import incremental_update


def retrieve_code(query: str, retriever) -> str:
    """Retrieve relevant code snippets using the LlamaIndex retriever."""
    nodes = retriever.retrieve(query)
    return "\n\n".join(n.get_content() for n in nodes)


def generate_prompt(code: str, history: str) -> str:
    """Fill the chat prompt template with code snippet & git history."""
    return REFRACTOR_PROMPT.format(code=code, history=history)


def call_llm(prompt: str, llm) -> str:
    """Invoke the LangChain LLM and return text content only."""
    response = llm([HumanMessage(content=prompt)])
    return response.content


def answer(query: str, retriever, llm) -> str:
    """High‑level helper that wires all steps together."""
    # 1) ensure index is up‑to‑date
    try:
        incremental_update()
    except Exception as e:
        print(f"[core_chat] incremental_update failed: {e}")

    # 2) retrieve code & git history
    code_snippet = retrieve_code(query, retriever)
    history = "\n".join(
        f"* {c['message']} ({c['author']}, {c['date']})"
        for c in commit_messages(5)
    )

    # 3) compose prompt & ask LLM
    prompt = generate_prompt(code_snippet, history)
    try:
        return call_llm(prompt, llm)
    except Exception as e:
        print(f"[core_chat] LLM call failed: {e}")
        return "❌ 内部エラーが発生しました。ログをご確認ください。"
