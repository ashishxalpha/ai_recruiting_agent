from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.application.schemas.common import StandardResponseDTO, create_response
from src.application.schemas.dashboard import RecentActivityDTO
from src.infrastructure.database.models import (
    AuditLogModel,
    CandidateModel,
    JobRequirementModel,
    RecruiterFeedbackModel
)

class RecentActivityQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_recent_activity(self, limit: int = 20) -> StandardResponseDTO[RecentActivityDTO]:
        activities: List[Dict[str, Any]] = []

        # 1. Fetch from Audit Logs
        stmt_audit = (
            select(AuditLogModel)
            .order_by(AuditLogModel.created_at.desc())
            .limit(limit)
        )
        res_audit = await self.session.execute(stmt_audit)
        for log in res_audit.scalars().all():
            action_desc = log.action.replace("_", " ").title()
            activities.append({
                "event_id": str(log.id),
                "description": f"{log.entity_type} {action_desc}",
                "source": "AUDIT",
                "timestamp": log.created_at.isoformat() if log.created_at else None
            })

        # 2. Fetch Recent Candidates
        stmt_cand = (
            select(CandidateModel)
            .order_by(CandidateModel.created_at.desc())
            .limit(limit)
        )
        res_cand = await self.session.execute(stmt_cand)
        for cand in res_cand.scalars().all():
            cand_name = f"{cand.first_name or ''} {cand.last_name or ''}".strip() or "New Candidate"
            activities.append({
                "event_id": str(cand.id),
                "description": f"Candidate profile ingested: {cand_name}",
                "source": "INGESTION",
                "timestamp": cand.created_at.isoformat() if cand.created_at else None
            })

        # 3. Fetch Recent Job Requirements
        stmt_jobs = (
            select(JobRequirementModel)
            .order_by(JobRequirementModel.created_at.desc())
            .limit(limit)
        )
        res_jobs = await self.session.execute(stmt_jobs)
        for job in res_jobs.scalars().all():
            activities.append({
                "event_id": str(job.id),
                "description": f"Job requisition opened: {job.title}",
                "source": "REQUISITION",
                "timestamp": job.created_at.isoformat() if job.created_at else None
            })

        # 4. Fetch Recent Recruiter Feedback
        stmt_fb = (
            select(RecruiterFeedbackModel)
            .order_by(RecruiterFeedbackModel.created_at.desc())
            .limit(limit)
        )
        res_fb = await self.session.execute(stmt_fb)
        for fb in res_fb.scalars().all():
            decision_text = fb.decision.value if hasattr(fb.decision, 'value') else str(fb.decision)
            activities.append({
                "event_id": str(fb.id),
                "description": f"Recruiter feedback recorded: {decision_text}",
                "source": "FEEDBACK",
                "timestamp": fb.created_at.isoformat() if fb.created_at else None
            })

        # Sort combined activities by timestamp descending
        activities = [a for a in activities if a["timestamp"] is not None]
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        activities = activities[:limit]

        data = RecentActivityDTO(activities=activities)
        return create_response(
            data=data,
            feature_available=True,
            data_available=len(activities) > 0,
            message="Recent activities retrieved successfully." if activities else "No recent activity recorded."
        )
