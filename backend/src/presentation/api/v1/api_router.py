from fastapi import APIRouter
from .endpoints import resumes, documents, candidates, jobs, extractions, search, feedback, outcomes, analytics, stream, workflows, memory, tools, agents, coordinator, organization

api_router = APIRouter()

api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(extractions.router, prefix="/extractions", tags=["extractions"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(feedback.router, tags=["feedback"])
api_router.include_router(outcomes.router, tags=["outcomes"])
api_router.include_router(analytics.router, tags=["analytics"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(coordinator.router, prefix="/coordinator", tags=["coordinator"])
api_router.include_router(organization.router, prefix="/organization", tags=["organization"])
