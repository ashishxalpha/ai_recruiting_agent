import structlog
from typing import List
from openai import AsyncOpenAI
import time

from src.domain.interfaces.embedding import EmbeddingProvider

logger = structlog.get_logger(__name__)

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small", version: str = "v1"):
        self.client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._version = version

    async def generate_embedding(self, text: str) -> List[float]:
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self._model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Failed to generate embedding", error=str(e))
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self._model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error("Failed to generate embeddings batch", error=str(e))
            raise

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def embedding_version(self) -> str:
        return self._version
