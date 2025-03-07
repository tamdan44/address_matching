from langchain_openai import ChatOpenAI

def load_llm(api_key: str, temp: float, model: str) -> ChatOpenAI:
    """Load the LLM model with the given API key and parameters."""
    return ChatOpenAI(openai_api_key=api_key, temperature=temp, model=model)

