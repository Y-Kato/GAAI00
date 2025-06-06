from core_chat import answer

class ChatSession:
    """Lightweight session manager shared by UI layers."""

    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
        self.history = []  # optional simple history tracking

    def respond(self, message: str) -> str:
        reply = answer(message, self.retriever, self.llm)
        self.history.append({"user": message, "bot": reply})
        return reply
