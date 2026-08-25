import uuid
import logging
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.errors import NodeInterrupt

from src.application.workflows.interfaces import WorkflowDefinition, CheckpointStore
from src.application.workflows.state import RecruitingWorkflowState
from src.infrastructure.database.models import (
    JobRequirementModel, CandidateModel, CandidateMatchModel, MatchExplanationModel
)
from src.infrastructure.providers.ai.openai import OpenAIExtractionProvider
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

class OutreachWorkflowState(RecruitingWorkflowState):
    draft_email_content: str
    email_status: str

class OutreachWorkflowDefinition(WorkflowDefinition):
    name: str = "outreach_agent"
    version: str = "v1"
    configuration: Dict[str, Any] = {}
    supported_states: List[str] = ["PENDING", "RUNNING", "PAUSED", "COMPLETED", "FAILED"]
    required_capabilities: List[str] = ["llm"]

    def __init__(self, ai_provider: OpenAIExtractionProvider, db_session_maker):
        self.ai_provider = ai_provider
        self.db_session_maker = db_session_maker

    def compile(self, checkpointer: CheckpointStore = None) -> Any:
        workflow = StateGraph(OutreachWorkflowState)

        # Nodes
        workflow.add_node("fetch_context", self._fetch_context)
        workflow.add_node("draft_email", self._draft_email)
        workflow.add_node("human_review", self._human_review)
        workflow.add_node("send_email", self._send_email)

        # Edges
        workflow.set_entry_point("fetch_context")
        workflow.add_edge("fetch_context", "draft_email")
        workflow.add_edge("draft_email", "human_review")
        workflow.add_edge("human_review", "send_email")
        workflow.add_edge("send_email", END)

        return workflow.compile(checkpointer=checkpointer)

    async def _fetch_context(self, state: OutreachWorkflowState) -> OutreachWorkflowState:
        logger.info("OutreachAgent: Fetching context...")
        job_id = state.get("job_id")
        candidate_id = state.get("candidate_id")

        if not job_id or not candidate_id:
            raise ValueError("job_id and candidate_id are required in state")

        async with self.db_session_maker() as session:
            # 1. Fetch Job
            job = (await session.execute(
                select(JobRequirementModel).where(JobRequirementModel.id == uuid.UUID(job_id))
            )).scalar_one_or_none()

            # 2. Fetch Candidate
            candidate = (await session.execute(
                select(CandidateModel).where(CandidateModel.id == uuid.UUID(candidate_id))
            )).scalar_one_or_none()

            # 3. Fetch latest CandidateMatch
            match_stmt = (
                select(CandidateMatchModel, MatchExplanationModel)
                .outerjoin(MatchExplanationModel, MatchExplanationModel.candidate_match_id == CandidateMatchModel.id)
                .where(CandidateMatchModel.candidate_id == uuid.UUID(candidate_id))
                .order_by(desc(CandidateMatchModel.created_at))
                .limit(1)
            )
            match_res = (await session.execute(match_stmt)).first()

            if not job or not candidate:
                raise ValueError("Job or Candidate not found")

            match_data = None
            if match_res:
                cm, explanation = match_res
                match_data = {
                    "final_score": cm.final_score,
                    "strengths": explanation.strengths if explanation else [],
                    "gaps": explanation.gaps if explanation else []
                }

            state["metadata"] = state.get("metadata", {})
            state["metadata"]["job_context"] = {
                "title": job.title,
                "department": job.department,
                "company_name": "Autonomous Tech" # Mock or get from setting
            }
            state["metadata"]["candidate_context"] = {
                "name": f"{candidate.first_name} {candidate.last_name}",
                "email": candidate.email
            }
            if match_data:
                state["metadata"]["match_context"] = match_data

        return state

    async def _draft_email(self, state: OutreachWorkflowState) -> OutreachWorkflowState:
        logger.info("OutreachAgent: Drafting email...")
        job_ctx = state["metadata"].get("job_context", {})
        cand_ctx = state["metadata"].get("candidate_context", {})
        match_ctx = state["metadata"].get("match_context", {})

        prompt = f"""
        Draft a highly personalized outreach email to a candidate we want to interview.
        
        Candidate Name: {cand_ctx.get('name')}
        Job Title: {job_ctx.get('title')}
        Company: {job_ctx.get('company_name')}
        
        The AI Recruiter identified the following strengths for this candidate:
        {', '.join(match_ctx.get('strengths', [])) if match_ctx else 'Great overall profile.'}
        
        Write a professional, warm, and concise email. Do not include subject line placeholders, just write the email body.
        Mention their strengths specifically to show we actually read their profile.
        End with a call to action to schedule a 15-minute introductory call.
        """

        try:
            response = await self.ai_provider.client.chat.completions.create(
                model=self.ai_provider.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert technical recruiter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            email_body = response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Error drafting email: {e}")
            email_body = f"Hi {cand_ctx.get('name')},\n\nWe were really impressed with your profile for the {job_ctx.get('title')} role! Let's chat."

        state["draft_email_content"] = email_body
        state["email_status"] = "DRAFTED"
        return state

    def _human_review(self, state: OutreachWorkflowState) -> OutreachWorkflowState:
        logger.info("OutreachAgent: Pausing for human review...")
        from langgraph.types import interrupt
        
        if state.get("email_status") == "DRAFTED":
            user_review = interrupt("Please review the drafted email before sending.")
            if user_review:
                state["email_status"] = user_review.get("status", "APPROVED")
                if "draft_email_content" in user_review:
                    state["draft_email_content"] = user_review["draft_email_content"]
                    
        return state

    async def _send_email(self, state: OutreachWorkflowState) -> OutreachWorkflowState:
        logger.info("OutreachAgent: Sending email...")
        email_content = state.get("draft_email_content", "")
        logger.info(f"--- EMAIL SENT ---\n{email_content}\n------------------")
        
        state["email_status"] = "SENT"
        return state
