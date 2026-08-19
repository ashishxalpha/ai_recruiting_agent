import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

async def main():
    engine = create_async_engine("postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Get Job vector
        res = await session.execute(text("SELECT vector_data FROM job_requirement_embeddings WHERE job_requirement_id = 'a1a84da1-8aad-4545-b279-71b8ca84197e'"))
        row = res.fetchone()
        if not row:
            print("Job embedding not found")
            return
        job_vec = row[0]
        
        # Now query candidates
        stmt = text("SELECT candidate_id, vector_data <=> :vec AS distance FROM candidate_embeddings WHERE embedding_type = 'FULL_PROFILE' ORDER BY distance LIMIT 5")
        res = await session.execute(stmt, {"vec": job_vec})
        candidates = res.fetchall()
        for c in candidates:
            print(c)

if __name__ == "__main__":
    asyncio.run(main())
