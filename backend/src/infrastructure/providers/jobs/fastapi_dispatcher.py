import asyncio
from fastapi import BackgroundTasks
from src.domain.interfaces.providers import JobDispatcher
import logging

logger = logging.getLogger(__name__)

from src.infrastructure.workers.local_worker import execute_resume_extraction_job
import uuid

class FastAPIJobDispatcher(JobDispatcher):
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    async def dispatch(self, job_name: str, payload: dict) -> None:
        """
        In Sprint 4, we hook into real background workers.
        """
        logger.info(f"Dispatching job {job_name} with payload {payload}")
        
        job_id_str = payload.get("job_id")
        if job_name == "resume_extraction" and job_id_str:
            job_id = uuid.UUID(job_id_str)
            self.background_tasks.add_task(self._run_extraction_task, job_id)
        else:
            self.background_tasks.add_task(self._dummy_task, job_name, payload)
            
    async def _run_extraction_task(self, job_id: uuid.UUID):
        await execute_resume_extraction_job(job_id)
        
    async def _dummy_task(self, job_name: str, payload: dict):
        # A dummy simulation of job processing
        await asyncio.sleep(1)
        logger.info(f"Completed dummy processing for job {job_name}")
