import asyncio
from fastapi import BackgroundTasks
from src.domain.interfaces.providers import JobDispatcher
import logging
import uuid
from src.infrastructure.workers.local_worker import execute_resume_extraction_job

logger = logging.getLogger(__name__)

class FastAPIJobDispatcher(JobDispatcher):
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    async def dispatch(self, job_name: str, payload: dict) -> None:
        """
        Dispatches background jobs to real worker tasks.
        """
        logger.info(f"Dispatching job {job_name} with payload {payload}")
        
        job_id_str = payload.get("job_id")
        if not job_id_str:
            logger.error("job_id missing from payload")
            return
            
        job_id = uuid.UUID(job_id_str)
        
        if job_name == "resume_extraction":
            self.background_tasks.add_task(self._run_extraction_task, job_id)
        else:
            logger.warning(f"Unknown job_name: {job_name}, ignoring.")
            
    async def _run_extraction_task(self, job_id: uuid.UUID):
        await execute_resume_extraction_job(job_id)
