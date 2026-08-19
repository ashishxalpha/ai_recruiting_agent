import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

async def main():
    engine = create_async_engine("postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check CandidateMatches
        print("Search Sessions:")
        res = await session.execute(text("SELECT id, job_requirement_id FROM search_sessions"))
        rows = res.fetchall()
        for r in rows:
            print(f"- {r}")

        print("\nCandidate Matches:")
        res = await session.execute(text("SELECT id, search_session_id, candidate_id FROM candidate_matches"))
        rows = res.fetchall()
        for r in rows:
            print(f"- {r}")

if __name__ == "__main__":
    asyncio.run(main())
