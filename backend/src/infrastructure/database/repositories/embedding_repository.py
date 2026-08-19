from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.domain.entities import CandidateEmbedding
from src.infrastructure.database.models import CandidateEmbeddingModel

class CandidateEmbeddingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, entity: CandidateEmbedding) -> CandidateEmbeddingModel:
        return CandidateEmbeddingModel(
            id=entity.id,
            candidate_id=entity.candidate_id,
            embedding_type=entity.embedding_type,
            embedding_model=entity.embedding_model,
            embedding_version=entity.embedding_version,
            source_hash=entity.source_hash,
            vector_data=entity.vector_data,
            generated_at=entity.generated_at
        )

    async def create_batch(self, embeddings: List[CandidateEmbedding]) -> None:
        models = [self._to_model(e) for e in embeddings]
        self.session.add_all(models)
        await self.session.flush()

    async def get_by_candidate_id(self, candidate_id: str) -> List[CandidateEmbedding]:
        from sqlalchemy import select
        result = await self.session.execute(
            select(CandidateEmbeddingModel).where(CandidateEmbeddingModel.candidate_id == candidate_id)
        )
        models = result.scalars().all()
        return [
            CandidateEmbedding(
                id=m.id,
                candidate_id=m.candidate_id,
                embedding_type=m.embedding_type,
                embedding_model=m.embedding_model,
                embedding_version=m.embedding_version,
                source_hash=m.source_hash,
                vector_data=m.vector_data,
                generated_at=m.generated_at
            ) for m in models
        ]
