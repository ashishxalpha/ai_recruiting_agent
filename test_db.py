import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

async def main():
    engine = create_async_engine("postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check Candidate Embeddings
        print("Candidate Embeddings:")
        res = await session.execute(text("SELECT id, candidate_id, embedding_type FROM candidate_embeddings"))
        rows = res.fetchall()
        for r in rows:
            print(f"- {r}")
        print(f"Total candidate embeddings: {len(rows)}")

        # Check Job Requirement Embeddings
        print("\nJob Requirement Embeddings:")
        res = await session.execute(text("SELECT id, job_requirement_id, embedding_type FROM job_requirement_embeddings"))
        rows = res.fetchall()
        for r in rows:
            print(f"- {r}")
        print(f"Total job requirement embeddings: {len(rows)}")

        # Check Candidates
        print("\nCandidates:")
        res = await session.execute(text("SELECT id, first_name, last_name FROM candidates"))
        rows = res.fetchall()
        for r in rows:
            print(f"- {r}")
        print(f"Total candidates: {len(rows)}")

if __name__ == "__main__":
    asyncio.run(main())
