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
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"].get("checkpoint_id")

        from src.infrastructure.database.models import CheckpointModel
        from sqlalchemy import select, desc, and_

        if checkpoint_id:
            stmt = select(CheckpointModel).where(
                and_(
                    CheckpointModel.thread_id == thread_id,
                    CheckpointModel.checkpoint_ns == checkpoint_ns,
                    CheckpointModel.checkpoint_id == checkpoint_id
                )
            )
        else:
            stmt = select(CheckpointModel).where(
                and_(
                    CheckpointModel.thread_id == thread_id,
                    CheckpointModel.checkpoint_ns == checkpoint_ns
                )
            ).order_by(desc(CheckpointModel.checkpoint_id)).limit(1)

        result = await self.db.execute(stmt)
        record = result.scalars().first()

        if not record:
            return None

        # Return the exact CheckpointTuple expected by LangGraph
        return CheckpointTuple(
            config={
                "configurable": {
                    "thread_id": record.thread_id,
                    "checkpoint_ns": record.checkpoint_ns,
                    "checkpoint_id": record.checkpoint_id,
                }
            },
            checkpoint=record.checkpoint,
            metadata=record.metadata_,
            parent_config={
                "configurable": {
                    "thread_id": record.thread_id,
                    "checkpoint_ns": record.checkpoint_ns,
                    "checkpoint_id": record.parent_checkpoint_id,
                }
            } if record.parent_checkpoint_id else None
        )

    async def aput(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: ChannelVersions) -> dict:
        """Store the checkpoint."""
        from src.infrastructure.database.models import CheckpointModel
        from sqlalchemy.dialects.postgresql import insert

        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        
        # Determine parent_checkpoint_id if present
        # In a real implementation this might be tricky if not in config, but we try:
        parent_checkpoint_id = config["configurable"].get("checkpoint_id")

        stmt = insert(CheckpointModel).values(
            thread_id=thread_id,
            checkpoint_ns=checkpoint_ns,
            checkpoint_id=checkpoint["id"],
            parent_checkpoint_id=parent_checkpoint_id,
            type=metadata.get("type"),
            checkpoint=checkpoint,
            metadata_=metadata,
        ).on_conflict_do_update(
            index_elements=["thread_id", "checkpoint_ns", "checkpoint_id"],
            set_={
                "checkpoint": checkpoint,
                "metadata": metadata,
                "type": metadata.get("type")
            }
        )

        await self.db.execute(stmt)
        await self.db.flush()

        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint["id"]
            }
        }
        
    async def aput_writes(self, config: dict, writes: Sequence[Tuple[str, Any]], task_id: str) -> None:
        """Store pending checkpoint writes."""
        from src.infrastructure.database.models import CheckpointWriteModel
        from sqlalchemy.dialects.postgresql import insert
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"].get("checkpoint_id")
        
        if not checkpoint_id:
            raise ValueError("checkpoint_id is required to put writes")
            
        for idx, (channel, value) in enumerate(writes):
            stmt = insert(CheckpointWriteModel).values(
                thread_id=thread_id,
                checkpoint_ns=checkpoint_ns,
                checkpoint_id=checkpoint_id,
                task_id=task_id,
                idx=idx,
                channel=channel,
                type=None,
                value=value
            ).on_conflict_do_update(
                index_elements=["thread_id", "checkpoint_ns", "checkpoint_id", "task_id", "idx"],
                set_={
                    "channel": channel,
                    "value": value
                }
            )
            await self.db.execute(stmt)
            
        await self.db.flush()
        
    async def alist(self, config: dict, *, filter: dict = None, before: dict = None, limit: int = None) -> AsyncIterator[CheckpointTuple]:
        from src.infrastructure.database.models import CheckpointModel
        from sqlalchemy import select, desc, and_
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        
        stmt = select(CheckpointModel).where(
            and_(
                CheckpointModel.thread_id == thread_id,
                CheckpointModel.checkpoint_ns == checkpoint_ns
            )
        ).order_by(desc(CheckpointModel.checkpoint_id))
        
        if limit:
            stmt = stmt.limit(limit)
            
        result = await self.db.execute(stmt)
        records = result.scalars().all()
        
        for record in records:
            yield CheckpointTuple(
                config={
                    "configurable": {
                        "thread_id": record.thread_id,
                        "checkpoint_ns": record.checkpoint_ns,
                        "checkpoint_id": record.checkpoint_id,
                    }
                },
                checkpoint=record.checkpoint,
                metadata=record.metadata_,
                parent_config={
                    "configurable": {
                        "thread_id": record.thread_id,
                        "checkpoint_ns": record.checkpoint_ns,
                        "checkpoint_id": record.parent_checkpoint_id,
                    }
                } if record.parent_checkpoint_id else None
            )
