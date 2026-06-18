from dagster import ConfigurableResource
from langchain_ollama import OllamaEmbeddings


class EmbeddingResource(ConfigurableResource):
    base_url: str
    model_name: str

    def get_embeddings(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(
            model=self.model_name,
            base_url=self.base_url,
        )