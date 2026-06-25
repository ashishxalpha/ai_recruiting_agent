import json
from typing import Optional, Any, AsyncIterator, Tuple, Sequence, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata, CheckpointTuple, ChannelVersions
from src.application.workflows.interfaces import CheckpointStore

class DatabaseCheckpointStore(BaseCheckpointSaver, CheckpointStore):
    """
    Implements LangGraph's BaseCheckpointSaver for PostgreSQL,
    while also fulfilling the application's CheckpointStore interface.
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    # LangGraph Sync interface (not used usually in async contexts but required to implement or raise NotImplementedError)
    def put(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: ChannelVersions) -> dict:
        raise NotImplementedError("Use async methods")

    def get(self, config: dict) -> Optional[Checkpoint]:
        raise NotImplementedError("Use async methods")
        
    def get_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        raise NotImplementedError("Use async methods")
        
    def list(self, config: dict, *, limit: int = None, before: dict = None) -> Any:
        raise NotImplementedError("Use async methods")

    # Async implementation (Mock implementation for Sprint 8 - ideally this uses explicit SQLAlchemy models)
    async def aget_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        """Fetch the latest checkpoint for the given thread_id."""
        thread_id = config["configurable"]["thread_id"]
        # Dummy implementation that would normally fetch from `checkpoints` table
        return None

    async def aput(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: ChannelVersions) -> dict:
        """Store the checkpoint."""
        # Dummy implementation that would normally insert into `checkpoints` table
        # We assume the schema has thread_id, checkpoint_id, parent_id, checkpoint payload, metadata.
        return {
            "configurable": {
                "thread_id": config["configurable"]["thread_id"],
                "checkpoint_id": checkpoint["id"]
            }
        }
