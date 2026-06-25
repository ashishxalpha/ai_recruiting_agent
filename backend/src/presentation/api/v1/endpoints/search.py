from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.api.dependencies import get_db
from src.application.services.ranking_engine import CandidateRankingEngine
from src.domain.entities import CandidateMatchResult

router = APIRouter()

class SearchCandidatesRequest(BaseModel):
    job_requirement_id: UUID
    limit: Optional[int] = 10

@router.post("/candidates", response_model=List[CandidateMatchResult])
async def search_candidates(
    request: SearchCandidatesRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform a hybrid semantic search for candidates that match the given job requirement.
    Returns a ranked list of CandidateMatchResult containing a valid search_session_id.
    """
    engine = CandidateRankingEngine(session=db)
    results = await engine.rank_candidates(job_id=request.job_requirement_id, limit=request.limit)
    
    if results:
        from src.infrastructure.database.repositories.search_session_repository import SearchSessionRepository
        from src.infrastructure.database.repositories.candidate_match_repository import CandidateMatchRepository
        from src.application.services.match_persistence_service import CandidateMatchPersistenceService
        from src.infrastructure.events.event_bus import EventBus
        from src.domain.events import CandidateMatched
        import uuid
        from datetime import datetime
        
        session_repo = SearchSessionRepository(db)
        match_repo = CandidateMatchRepository(db)
        persistence = CandidateMatchPersistenceService(session_repo, match_repo)
        
        session_id = await persistence.persist_matches(request.job_requirement_id, results)
        await db.commit()
        
        # Publish Domain Event
        event = CandidateMatched(
            event_id=uuid.uuid4(),
            occurred_at=datetime.utcnow(),
            search_session_id=session_id,
            job_requirement_id=request.job_requirement_id,
            candidate_match_ids=[] # We don't have the match ids easily exposed in DTO right now, but we could map them. For now, empty list is fine for event scaffolding.
        )
        EventBus.publish(event)
        
    return results
