import pytest
import pytest_asyncio
import asyncio
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool
import os

from src.infrastructure.database.repositories.memory_repository import (
    SQLAlchemyMemoryMetadataRepository,
    SQLAlchemyMemoryVectorRepository,
    PostgresWorkingMemoryStore
)
from src.infrastructure.workflows.checkpoints.database import DatabaseCheckpointStore
from src.domain.memory_models import BaseMemory, MemoryNamespace, MemoryRetentionPolicy, MemorySource, WorkingMemory
from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://copilot:copilot_password@db:5432/ai_recruiting")

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_memory_metadata_repository(db_session):
    repo = SQLAlchemyMemoryMetadataRepository(db_session)
    
    memory_id = uuid4()
    source = MemorySource(source_id=uuid4(), source_type="test")
    memory = BaseMemory(
        id=memory_id,
        namespace=MemoryNamespace.SYSTEM,
        retention_policy=MemoryRetentionPolicy.PERMANENT,
        source=source
    )
    
    # 1. Save Memory
    await repo.save(memory)
    await db_session.commit()
    
    # 2. Get Memory
    retrieved = await repo.get(memory_id)
    assert retrieved is not None
    assert retrieved.id == memory_id
    assert retrieved.namespace == MemoryNamespace.SYSTEM
    
    # 3. Update Memory
    retrieved.importance = 0.99
    await repo.save(retrieved)
    await db_session.commit()
    
    updated = await repo.get(memory_id)
    assert updated.importance == 0.99
    
    # 4. Search Memory
    results = await repo.search("", {}, 10)
    assert isinstance(results, list)
    
    # 5. Delete Memory
    await repo.delete(memory_id)
    await db_session.commit()
    deleted = await repo.get(memory_id)
    assert deleted is None

@pytest.mark.asyncio
async def test_memory_vector_repository(db_session):
    meta_repo = SQLAlchemyMemoryMetadataRepository(db_session)
    memory_id = uuid4()
    source = MemorySource(source_id=uuid4(), source_type="test")
    memory = BaseMemory(id=memory_id, namespace=MemoryNamespace.SYSTEM, retention_policy=MemoryRetentionPolicy.PERMANENT, source=source)
    await meta_repo.save(memory)
    await db_session.commit()
    
    vector_repo = SQLAlchemyMemoryVectorRepository(db_session)
    
    embedding = [0.1] * 1536
    
    await vector_repo.upsert_embedding(
        memory_id=memory_id,
        embedding=embedding,
        model="text-embedding-3-small",
        version="v1",
        content_hash="testhash"
    )
    await db_session.commit()
    
    results = await vector_repo.search(query_embedding=embedding, filters={}, limit=5)
    assert len(results) > 0
    assert memory_id in results
    
    await vector_repo.delete_embedding(memory_id)
    await meta_repo.delete(memory_id)
    await db_session.commit()

@pytest.mark.asyncio
async def test_working_memory_store(db_session):
    store = PostgresWorkingMemoryStore(db_session)
    session_id = uuid4()
    
    wm = WorkingMemory(
        session_id=session_id,
        namespace=MemoryNamespace.SYSTEM,
        retention_policy=MemoryRetentionPolicy.SESSION,
        source=MemorySource(source_id=uuid4(), source_type="test"),
        volatile_state={"key": "value"}
    )
    
    await store.set_state(session_id, wm)
    await db_session.commit()
    
    retrieved = await store.get_state(session_id)
    assert retrieved is not None
    assert retrieved.volatile_state["key"] == "value"
    
    await store.clear_state(session_id)
    await db_session.commit()
    retrieved_after_clear = await store.get_state(session_id)
    assert retrieved_after_clear is None

@pytest.mark.asyncio
async def test_database_checkpoint_store(db_session):
    store = DatabaseCheckpointStore(db_session)
    
    thread_id = str(uuid4())
    checkpoint_id = str(uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_ns": ""
        }
    }
    
    checkpoint = {
        "v": 1,
        "id": checkpoint_id,
        "ts": "2026-01-01T00:00:00Z",
        "channel_values": {"test_channel": "test_value"},
        "channel_versions": {"test_channel": 1},
        "versions_seen": {},
        "pending_sends": []
    }
    
    metadata = {"source": "test", "step": 1, "writes": {}, "parents": {}}
    
    await store.aput(config, checkpoint, metadata, {})
    await db_session.commit()
    
    ct = await store.aget_tuple(config)
    assert ct is not None
    assert ct.checkpoint["id"] == checkpoint_id
    assert ct.checkpoint["channel_values"]["test_channel"] == "test_value"
    
    checkpoints = []
    async for c in store.alist(config):
        checkpoints.append(c)
        
    assert len(checkpoints) == 1
    assert checkpoints[0].checkpoint["id"] == checkpoint_id
    
    # Cleanup
    await db_session.execute(text(f"DELETE FROM checkpoints WHERE thread_id = '{thread_id}'"))
    await db_session.commit()
