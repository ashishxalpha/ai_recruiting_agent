import asyncio
import os
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata
from langgraph.checkpoint.base import CheckpointTuple
from typing import TypedDict, Annotated
import operator

from src.infrastructure.workflows.checkpoints.database import DatabaseCheckpointStore

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")

class State(TypedDict):
    messages: Annotated[list, operator.add]
    count: int

async def test_roundtrip():
    engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        store = DatabaseCheckpointStore(session)
        
        # We simulate what LangGraph does internally to save and fetch
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        checkpoint = {
            "v": 1,
            "id": str(uuid.uuid4()),
            "ts": "2026-01-01T00:00:00Z",
            "channel_values": {"messages": ["hello"], "count": 1},
            "channel_versions": {"messages": 1, "count": 1},
            "versions_seen": {},
            "pending_sends": []
        }
        
        metadata = {"source": "update", "step": 1, "writes": {}, "parents": {}}
        
        # Persist
        await store.aput(config, checkpoint, metadata, {})
        await session.commit()
        
        # Load
        loaded_tuple = await store.aget_tuple(config)
        print(f"Loaded Checkpoint ID: {loaded_tuple.checkpoint['id']}")
        assert loaded_tuple.checkpoint['id'] == checkpoint['id']
        assert loaded_tuple.checkpoint['channel_values']['count'] == 1
        
        # Resume and Persist Again
        new_checkpoint = dict(loaded_tuple.checkpoint)
        new_checkpoint['id'] = str(uuid.uuid4())
        new_checkpoint['channel_values']['count'] = 2
        new_checkpoint['channel_versions']['count'] = 2
        metadata['step'] = 2
        
        config["configurable"]["checkpoint_id"] = loaded_tuple.checkpoint['id'] # this becomes the parent
        
        await store.aput(config, new_checkpoint, metadata, {})
        await session.commit()
        
        # Load Latest
        latest_config = {"configurable": {"thread_id": thread_id}}
        latest_tuple = await store.aget_tuple(latest_config)
        
        print(f"Latest Checkpoint ID: {latest_tuple.checkpoint['id']}")
        assert latest_tuple.checkpoint['id'] == new_checkpoint['id']
        assert latest_tuple.checkpoint['channel_values']['count'] == 2
        print("Roundtrip Successful!")
        
        await session.execute(text(f"DELETE FROM checkpoints WHERE thread_id = '{thread_id}'"))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(test_roundtrip())
