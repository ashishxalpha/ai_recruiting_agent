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

    # Async implementation
    async def aget_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        """Fetch the latest checkpoint for the given thread_id."""
        from sqlalchemy import select
        from src.infrastructure.database.models import LangGraphCheckpointModel
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id")
        
        stmt = select(LangGraphCheckpointModel).where(LangGraphCheckpointModel.thread_id == thread_id)
        if checkpoint_id:
            stmt = stmt.where(LangGraphCheckpointModel.checkpoint_id == checkpoint_id)
        else:
            stmt = stmt.order_by(LangGraphCheckpointModel.checkpoint_id.desc()).limit(1)
            
        result = await self.db.execute(stmt)
        record = result.scalar_one_or_none()
        
        if not record:
            return None
            
        # LangGraph serde outputs bytes, so we parse JSONB back to bytes for deserialization
        checkpoint = self.serde.loads(json.dumps(record.checkpoint_payload).encode('utf-8'))
        metadata = self.serde.loads(json.dumps(record.metadata_payload).encode('utf-8'))
        
        return CheckpointTuple(
            config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.checkpoint_id}},
            checkpoint=checkpoint,
            metadata=metadata,
            parent_config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.parent_checkpoint_id}} if record.parent_checkpoint_id else None
        )

    async def aput(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: ChannelVersions) -> dict:
        """Store the checkpoint."""
        from src.infrastructure.database.models import LangGraphCheckpointModel
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]
        
        chk_str = self.serde.dumps(checkpoint).decode('utf-8')
        meta_str = self.serde.dumps(metadata).decode('utf-8')
        
        record = LangGraphCheckpointModel(
            thread_id=thread_id,
            checkpoint_id=checkpoint_id,
            parent_checkpoint_id=config["configurable"].get("checkpoint_id"),
            checkpoint_payload=json.loads(chk_str),
            metadata_payload=json.loads(meta_str)
        )
        self.db.add(record)
        await self.db.commit()
        
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint_id
            }
        }
        
    async def alist(self, config: dict, *, filter: dict = None, before: dict = None, limit: int = None) -> AsyncIterator[CheckpointTuple]:
        from sqlalchemy import select
        from src.infrastructure.database.models import LangGraphCheckpointModel
        
        thread_id = config["configurable"]["thread_id"]
        stmt = select(LangGraphCheckpointModel).where(LangGraphCheckpointModel.thread_id == thread_id)
        
        stmt = stmt.order_by(LangGraphCheckpointModel.checkpoint_id.desc())
        if limit:
            stmt = stmt.limit(limit)
            
        result = await self.db.execute(stmt)
        records = result.scalars().all()
        
        for record in records:
            checkpoint = self.serde.loads(json.dumps(record.checkpoint_payload).encode('utf-8'))
            metadata = self.serde.loads(json.dumps(record.metadata_payload).encode('utf-8'))
            yield CheckpointTuple(
                config={"configurable": {"thread_id": record.thread_id, "checkpoint_id": record.checkpoint_id}},
                checkpoint=checkpoint,
                metadata=metadata,
                parent_config={"configurable": {"thread_id": record.thread_id, "checkpoint_id": record.parent_checkpoint_id}} if record.parent_checkpoint_id else None
            )
