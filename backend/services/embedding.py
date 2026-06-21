# Embeds user query using nomic-embed-text via Ollama

from langchain_ollama import OllamaEmbeddings
from core.config import OLLAMA_HOST, EMBEDDING_MODEL


def get_embedding_model() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_HOST
    )


def embed_query(query: str) -> list[float]:
    model = get_embedding_model()
    return model.embed_query(query)