from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import Dict, Any

from src.application.services.analytics.provider import AnalyticsProvider
from src.infrastructure.database.models import (
    CandidateMatchModel,
    RecruiterFeedbackModel,
    GroundTruthEventModel
)

class RealtimeAnalyticsProvider(AnalyticsProvider):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_job_analytics(self, job_id: UUID) -> Dict[str, Any]:
        # Count total matches for this job (via search sessions)
        from src.infrastructure.database.models import SearchSessionModel
        
        stmt = (
            select(func.count(CandidateMatchModel.id))
            .join(SearchSessionModel, CandidateMatchModel.search_session_id == SearchSessionModel.id)
            .where(SearchSessionModel.job_requirement_id == job_id)
        )
        total_matches = await self.session.scalar(stmt) or 0

        # Group feedback decisions
        stmt = (
            select(RecruiterFeedbackModel.decision, func.count(RecruiterFeedbackModel.id))
            .join(CandidateMatchModel, RecruiterFeedbackModel.candidate_match_id == CandidateMatchModel.id)
            .join(SearchSessionModel, CandidateMatchModel.search_session_id == SearchSessionModel.id)
            .where(SearchSessionModel.job_requirement_id == job_id)
            .group_by(RecruiterFeedbackModel.decision)
        )
        res = await self.session.execute(stmt)
        decisions = dict(res.all())

        return {
            "total_matches": total_matches,
            "approved": decisions.get("APPROVED", 0),
            "rejected": decisions.get("REJECTED", 0),
            "shortlisted": decisions.get("SHORTLISTED", 0),
            "interviews": decisions.get("INTERVIEW", 0),
            "maybe": decisions.get("MAYBE", 0)
        }

    async def get_evaluation_metrics(self) -> Dict[str, Any]:
        # System-wide metrics
        # 1. Recruiter Agreement Rate (Fraction of AI matches where Recruiter Decision is positive)
        # Note: A simple implementation is Approval Rate + Shortlisted + Interview / Total Feedback
        stmt_fb = select(RecruiterFeedbackModel.decision, func.count(RecruiterFeedbackModel.id)).group_by(RecruiterFeedbackModel.decision)
        fb_res = await self.session.execute(stmt_fb)
        decisions = dict(fb_res.all())
        total_fb = sum(decisions.values())
        
        positives = decisions.get("APPROVED", 0) + decisions.get("SHORTLISTED", 0) + decisions.get("INTERVIEW", 0)
        agreement_rate = positives / total_fb if total_fb > 0 else 0.0
        approval_rate = decisions.get("APPROVED", 0) / total_fb if total_fb > 0 else 0.0
        interview_rate = decisions.get("INTERVIEW", 0) / total_fb if total_fb > 0 else 0.0

        # Hire Conversion Rate (Hired / Total Ground Truth Events with HIRED vs Total uniquely tracked candidates)
        stmt_hires = select(func.count(GroundTruthEventModel.id)).where(GroundTruthEventModel.event_type == "HIRED")
        hires = await self.session.scalar(stmt_hires) or 0
        
        # Unique candidates who applied or started funnel
        stmt_candidates = select(func.count(func.distinct(GroundTruthEventModel.candidate_id)))
        total_candidates = await self.session.scalar(stmt_candidates) or 0
        
        hire_rate = hires / total_candidates if total_candidates > 0 else 0.0

        # Avg Match Score
        stmt_avg_score = select(func.avg(CandidateMatchModel.final_score))
        avg_score = await self.session.scalar(stmt_avg_score) or 0.0

        return {
            "recruiter_agreement_rate": round(agreement_rate, 4),
            "approval_rate": round(approval_rate, 4),
            "interview_rate": round(interview_rate, 4),
            "hire_rate": round(hire_rate, 4),
            "average_match_score": round(avg_score, 4),
            "average_processing_time": 0.0, # Placeholder
            "average_embedding_latency": 0.0 # Placeholder
        }
