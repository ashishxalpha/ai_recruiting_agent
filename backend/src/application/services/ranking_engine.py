from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from uuid import UUID

from src.domain.entities import CandidateMatchResult, JobRequirement
from src.infrastructure.database.models import (
    CandidateEmbeddingModel, 
    JobRequirementEmbeddingModel,
    CandidateModel,
    AIExtractionModel
)
from src.domain.enums import EmbeddingType

class CandidateRankingEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_job_embeddings(self, job_id: UUID) -> Dict[str, Any]:
        """Fetch all embeddings for a job requirement."""
        stmt = select(JobRequirementEmbeddingModel).where(JobRequirementEmbeddingModel.job_requirement_id == job_id)
        result = await self.session.execute(stmt)
        embeddings = result.scalars().all()
        return {e.embedding_type: e.vector_data for e in embeddings}

    async def rank_candidates(self, job_id: UUID, limit: int = 10) -> List[CandidateMatchResult]:
        """
        Rank candidates using hybrid scoring:
        - FULL_PROFILE Vector Similarity (40%)
        - SKILLS Match (25%)
        - EXPERIENCE Match (20%)
        - EDUCATION Match (10%)
        - Profile Quality (5%)
        """
        job_embeddings = await self._get_job_embeddings(job_id)
        
        # If no full profile embedding, we can't do vector search
        if EmbeddingType.FULL_PROFILE.value not in job_embeddings:
            return []

        full_profile_vector = job_embeddings[EmbeddingType.FULL_PROFILE.value]

        # Fetch candidates based on FULL_PROFILE similarity (top N candidates)
        # Using pgvector cosine distance `<=>`. Distance is 1 - similarity.
        distance_col = CandidateEmbeddingModel.vector_data.cosine_distance(full_profile_vector)
        stmt = (
            select(CandidateEmbeddingModel.candidate_id, distance_col.label("distance"))
            .where(CandidateEmbeddingModel.embedding_type == EmbeddingType.FULL_PROFILE.value)
            .order_by(distance_col)
            .limit(limit * 2) # Fetch extra to rerank
        )
        
        result = await self.session.execute(stmt)
        candidates = result.all()

        results = []
        for candidate_id, distance in candidates:
            # 1. Vector Similarity (FULL_PROFILE)
            semantic_score = max(0.0, 1.0 - distance)

            # Fetch candidate embeddings for specific matches
            c_stmt = select(CandidateEmbeddingModel).where(CandidateEmbeddingModel.candidate_id == candidate_id)
            c_res = await self.session.execute(c_stmt)
            c_embeddings = {e.embedding_type: e.vector_data for e in c_res.scalars().all()}

            def calculate_similarity(e_type: str) -> float:
                if e_type in job_embeddings and e_type in c_embeddings:
                    # manual cosine similarity calculation could be done here, or assumed fetched from DB.
                    # for simplicity, we will just assume 0.5 if we can't compute it in SQL right now, 
                    # but actually we can compute it using dot product or we just fetch it.
                    # Since we have the vectors in memory here:
                    import numpy as np
                    v1 = np.array(job_embeddings[e_type])
                    v2 = np.array(c_embeddings[e_type])
                    dot = np.dot(v1, v2)
                    norm1 = np.linalg.norm(v1)
                    norm2 = np.linalg.norm(v2)
                    if norm1 > 0 and norm2 > 0:
                        return float(dot / (norm1 * norm2))
                return 0.0

            # 2. Skills Match
            skills_score = calculate_similarity(EmbeddingType.SKILLS.value)
            
            # 3. Experience Match
            experience_score = calculate_similarity(EmbeddingType.EXPERIENCE.value)
            
            # 4. Education Match
            education_score = calculate_similarity(EmbeddingType.EDUCATION.value)

            # 5. Profile Quality (from AIExtraction)
            pq_stmt = select(AIExtractionModel.overall_confidence).where(
                AIExtractionModel.document.has(candidate_id=candidate_id)
            ).order_by(desc(AIExtractionModel.created_at)).limit(1)
            pq_res = await self.session.execute(pq_stmt)
            pq_val = pq_res.scalar()
            profile_quality_score = float(pq_val) if pq_val is not None else 0.5

            # Calculate Final Score
            final_score = (
                (semantic_score * 0.40) +
                (skills_score * 0.25) +
                (experience_score * 0.20) +
                (education_score * 0.10) +
                (profile_quality_score * 0.05)
            )

            # Generate strengths and gaps based on scores
            strengths = []
            gaps = []
            if skills_score > 0.8: strengths.append("Strong skills match")
            elif skills_score < 0.4: gaps.append("Skills gap detected")
            
            if experience_score > 0.8: strengths.append("Highly relevant experience")
            elif experience_score < 0.4: gaps.append("Experience may not align")

            if semantic_score > 0.85: strengths.append("Excellent overall profile fit")

            recommendations = []
            if final_score > 0.75: recommendations.append("Highly recommended for interview")
            elif final_score > 0.6: recommendations.append("Consider for review")

            match_result = CandidateMatchResult(
                candidate_id=candidate_id,
                job_requirement_id=job_id,
                semantic_score=semantic_score,
                skills_score=skills_score,
                experience_score=experience_score,
                education_score=education_score,
                final_score=final_score,
                strengths=strengths,
                gaps=gaps,
                recommendations=recommendations
            )
            results.append(match_result)

        # Sort by final hybrid score
        results.sort(key=lambda x: x.final_score, reverse=True)
        return results[:limit]
