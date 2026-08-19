import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.infrastructure.database.models import (
    CandidateEmbeddingModel, 
    JobRequirementEmbeddingModel,
    CandidateModel,
    JobRequirementModel
)
from src.domain.enums import EmbeddingType
from src.infrastructure.providers.ai.openai import OpenAIExtractionProvider
from src.application.services.match_persistence_service import CandidateMatchPersistenceService
from src.domain.entities import CandidateMatchResult
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class CandidateMatchingService:
    def __init__(self, db: AsyncSession, ai_provider: OpenAIExtractionProvider, persistence_service: CandidateMatchPersistenceService):
        self.db = db
        self.ai_provider = ai_provider
        self.persistence_service = persistence_service

    async def run_semantic_match(self, job_requirement_id: uuid.UUID, top_k: int = 5) -> uuid.UUID:
        """
        Runs a semantic match between a job requirement and all candidates.
        Returns the SearchSession ID.
        """
        with tracer.start_as_current_span("CandidateMatchingService.run_semantic_match"):
            # 1. Fetch Job Requirement and its Embedding
            job_stmt = select(JobRequirementModel).where(JobRequirementModel.id == job_requirement_id)
            job_result = await self.db.execute(job_stmt)
            job = job_result.scalar_one_or_none()
            if not job:
                raise ValueError("Job requirement not found")

            job_embed_stmt = select(JobRequirementEmbeddingModel).where(
                JobRequirementEmbeddingModel.job_requirement_id == job_requirement_id,
                JobRequirementEmbeddingModel.embedding_type == EmbeddingType.FULL_PROFILE.value
            )
            job_embed_result = await self.db.execute(job_embed_stmt)
            job_embedding = job_embed_result.scalar_one_or_none()
            
            if not job_embedding:
                raise ValueError("Job requirement embedding not found. Cannot perform matching.")

            vector = job_embedding.vector_data

            # 2. Query pgvector for closest candidates (Cosine Similarity <->)
            # pgvector cosine distance operator is <=> 
            # similarity = 1 - distance
            # We want to order by distance ASC (closest first)
            
            match_stmt = (
                select(
                    CandidateEmbeddingModel.candidate_id, 
                    CandidateEmbeddingModel.vector_data.cosine_distance(vector).label("distance")
                )
                .where(CandidateEmbeddingModel.embedding_type == EmbeddingType.FULL_PROFILE.value)
                .order_by("distance")
                .limit(top_k)
            )
            
            match_results = await self.db.execute(match_stmt)
            top_candidates = match_results.all()

            if not top_candidates:
                # No candidates with embeddings
                return await self.persistence_service.persist_matches(job_requirement_id, [])

            # 3. For the top candidates, fetch their full profile and ask OpenAI to evaluate
            candidate_ids = [row.candidate_id for row in top_candidates]
            candidates_stmt = select(CandidateModel).options(
                selectinload(CandidateModel.skills),
                selectinload(CandidateModel.experience),
                selectinload(CandidateModel.education)
            ).where(CandidateModel.id.in_(candidate_ids))
            
            candidates_result = await self.db.execute(candidates_stmt)
            candidates_map = {c.id: c for c in candidates_result.scalars().all()}

            results: List[CandidateMatchResult] = []

            job_text = f"Title: {job.title}\nDescription: {job.description}\nSkills: {', '.join(job.skills_required)}\nExperience: {job.experience_required}"

            for row in top_candidates:
                c_id = row.candidate_id
                distance = float(row.distance)
                semantic_score = 1.0 - distance # Convert distance to similarity score
                
                candidate = candidates_map.get(c_id)
                if not candidate:
                    continue
                    
                # Construct candidate text
                c_text = f"Name: {candidate.first_name} {candidate.last_name}\nSummary: {candidate.summary}\n"
                c_text += "Skills: " + ", ".join([s.name for s in candidate.skills]) + "\n"
                c_text += "Experience:\n" + "\n".join([f"{e.title} at {e.company}: {e.description}" for e in candidate.experience]) + "\n"
                c_text += "Education:\n" + "\n".join([f"{e.degree} at {e.institution}" for e in candidate.education])
                
                # Call OpenAI for deeper evaluation
                evaluation = await self._evaluate_with_ai(job_text, c_text)
                
                ai_score = evaluation.get("match_score", 0.0) / 100.0
                # Hybrid score: 40% semantic, 60% AI
                final_score = (semantic_score * 0.4) + (ai_score * 0.6)
                
                result = CandidateMatchResult(
                    candidate_id=c_id,
                    job_requirement_id=job_requirement_id,
                    semantic_score=semantic_score,
                    skills_score=evaluation.get("skills_score", 0.0) / 100.0,
                    experience_score=evaluation.get("experience_score", 0.0) / 100.0,
                    education_score=0.0,
                    final_score=final_score,
                    strengths=evaluation.get("strengths", []),
                    gaps=evaluation.get("gaps", []),
                    recommendations=[evaluation.get("recommendation", "None")]
                )
                results.append(result)

            # Sort by final score
            results.sort(key=lambda x: x.final_score, reverse=True)

            # 4. Persist
            session_id = await self.persistence_service.persist_matches(job_requirement_id, results)
            await self.db.commit()
            return session_id

    async def _evaluate_with_ai(self, job_text: str, candidate_text: str) -> Dict[str, Any]:
        """
        Uses OpenAI to generate strengths, gaps, and a match score.
        """
        prompt = f"""
You are an expert technical recruiter. Evaluate the following candidate against the job requirement.

JOB REQUIREMENT:
{job_text}

CANDIDATE PROFILE:
{candidate_text}

Provide your evaluation in the following JSON schema:
{{
    "match_score": integer (0-100, overall fit),
    "skills_score": integer (0-100, how well skills match),
    "experience_score": integer (0-100, how well experience matches),
    "strengths": [array of short strings highlighting why they are a good fit],
    "gaps": [array of short strings highlighting missing requirements],
    "recommendation": string (One sentence summary recommendation)
}}
"""
        try:
            import json
            response = await self.ai_provider.client.chat.completions.create(
                model=self.ai_provider.model_name,
                messages=[
                    {"role": "system", "content": "You are a JSON-outputting recruiter assistant. Always output valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=0.1
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {
                "match_score": 50,
                "skills_score": 50,
                "experience_score": 50,
                "strengths": ["Failed to generate AI evaluation"],
                "gaps": [],
                "recommendation": f"Error: {str(e)}"
            }
