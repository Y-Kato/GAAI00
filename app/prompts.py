from langchain.prompts import ChatPromptTemplate

REFRACTOR_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert software architect. Given the following source snippet and its git history context, propose clear, actionable refactor suggestions that improve readability, modularity, and maintainability without changing behaviour.

    ## Snippet
    ```
    {code}
    ```

    ## Commit history context
    {history}

    Respond in Japanese as bullet points.
    """
)