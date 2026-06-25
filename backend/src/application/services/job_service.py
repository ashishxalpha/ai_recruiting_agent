from uuid import UUID
from typing import Optional

from src.domain.entities import BackgroundJob
from src.domain.enums import JobStatus
from src.domain.interfaces.repositories import JobRepository
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class BackgroundJobService:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    async def get_job(self, job_id: UUID) -> Optional[BackgroundJob]:
        with tracer.start_as_current_span("BackgroundJobService.get_job"):
            return await self.job_repo.get_by_id(job_id)

    async def update_status(self, job_id: UUID, status: JobStatus, error_message: Optional[str] = None) -> Optional[BackgroundJob]:
        with tracer.start_as_current_span("BackgroundJobService.update_status"):
            job = await self.job_repo.get_by_id(job_id)
            if not job:
                return None
            job.status = status
            if error_message:
                job.error_message = error_message
            return await self.job_repo.update(job)
