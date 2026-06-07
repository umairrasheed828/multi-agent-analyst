from langchain_openai import ChatOpenAI

from src.config import settings


def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """Shared LLM client. temperature=0 for deterministic, auditable behavior."""
    return ChatOpenAI(model=settings.llm_model, temperature=temperature)
