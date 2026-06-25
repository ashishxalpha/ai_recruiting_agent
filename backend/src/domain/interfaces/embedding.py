from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate a single embedding for the given text."""
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate multiple embeddings for the given texts."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name used for embeddings."""
        pass

    @property
    @abstractmethod
    def embedding_version(self) -> str:
        """Return the version of the embedding logic/model."""
        pass
