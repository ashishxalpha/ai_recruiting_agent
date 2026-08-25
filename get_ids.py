import asyncio
from sqlalchemy import select
from src.infrastructure.database.base import async_session_maker
from src.infrastructure.database.models import JobRequirementModel, CandidateModel

async def main():
    async with async_session_maker() as session:
        job = (await session.execute(select(JobRequirementModel).limit(1))).scalar_one_or_none()
        candidate = (await session.execute(select(CandidateModel).limit(1))).scalar_one_or_none()
        if job and candidate:
            print(f"JOB_ID={job.id}")
            print(f"CANDIDATE_ID={candidate.id}")
        else:
            print("Missing job or candidate")

asyncio.run(main())
