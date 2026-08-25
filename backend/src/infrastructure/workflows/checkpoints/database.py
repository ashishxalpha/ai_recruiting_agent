import json
from typing import Optional, Any, AsyncIterator, Tuple, Sequence, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata, CheckpointTuple, ChannelVersions
from src.application.workflows.interfaces import CheckpointStore

from typing import Callable

class DatabaseCheckpointStore(BaseCheckpointSaver, CheckpointStore):
    """
    Implements LangGraph's BaseCheckpointSaver for PostgreSQL,
    while also fulfilling the application's CheckpointStore interface.
    """
    
    def __init__(self, session_maker: Callable[[], AsyncSession]):
        super().__init__()
        self.session_maker = session_maker

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
        import base64
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id")
        
        async with self.session_maker() as db:
            stmt = select(LangGraphCheckpointModel).where(LangGraphCheckpointModel.thread_id == thread_id)
            if checkpoint_id:
                stmt = stmt.where(LangGraphCheckpointModel.checkpoint_id == checkpoint_id)
            else:
                stmt = stmt.order_by(LangGraphCheckpointModel.checkpoint_id.desc()).limit(1)
                
            result = await db.execute(stmt)
            record = result.scalar_one_or_none()
            
            if not record:
                return None
                
            chk_type = record.checkpoint_payload.get("type", "json")
            chk_bytes = base64.b64decode(record.checkpoint_payload["payload"])
            checkpoint = self.serde.loads_typed((chk_type, chk_bytes))
            
            meta_type = record.metadata_payload.get("type", "json")
            meta_bytes = base64.b64decode(record.metadata_payload["payload"])
            metadata = self.serde.loads_typed((meta_type, meta_bytes))
            
            # Fetch pending writes
            from src.infrastructure.database.models import CheckpointWriteModel
            stmt_writes = select(CheckpointWriteModel).where(
                CheckpointWriteModel.thread_id == thread_id,
                CheckpointWriteModel.checkpoint_id == record.checkpoint_id
            )
            writes_result = await db.execute(stmt_writes)
            write_records = writes_result.scalars().all()
            
            pending_writes = []
            for w in write_records:
                val_bytes = base64.b64decode(w.value["payload"])
                val = self.serde.loads_typed((w.type, val_bytes))
                pending_writes.append((w.task_id, w.channel, val))
            
            return CheckpointTuple(
                config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.checkpoint_id}},
                checkpoint=checkpoint,
                metadata=metadata,
                parent_config={"configurable": {"thread_id": thread_id, "checkpoint_id": record.parent_checkpoint_id}} if record.parent_checkpoint_id else None,
                pending_writes=pending_writes if pending_writes else None
            )

    async def aput_writes(
        self,
        config: dict,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store pending writes."""
        from src.infrastructure.database.models import CheckpointWriteModel
        from sqlalchemy.dialects.postgresql import insert
        from langgraph.checkpoint.base import WRITES_IDX_MAP
        import base64
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"]["checkpoint_id"]
        
        async with self.session_maker() as db:
            for idx, (channel, value) in enumerate(writes):
                val_type, val_bytes = self.serde.dumps_typed(value)
                mapped_idx = WRITES_IDX_MAP.get(channel, idx)
                
                stmt = insert(CheckpointWriteModel).values(
                    thread_id=thread_id,
                    checkpoint_ns=checkpoint_ns,
                    checkpoint_id=checkpoint_id,
                    task_id=task_id,
                    idx=mapped_idx,
                    channel=channel,
                    type=val_type,
                    value={
                        "payload": base64.b64encode(val_bytes).decode("ascii")
                    }
                )
                stmt = stmt.on_conflict_do_update(
                    index_elements=['thread_id', 'checkpoint_ns', 'checkpoint_id', 'task_id', 'idx'],
                    set_=dict(
                        channel=stmt.excluded.channel,
                        type=stmt.excluded.type,
                        value=stmt.excluded.value
                    )
                )
                await db.execute(stmt)
            await db.commit()

    async def aput(self, config: dict, checkpoint: Checkpoint, metadata: CheckpointMetadata, new_versions: ChannelVersions) -> dict:
        """Store the checkpoint."""
        from src.infrastructure.database.models import LangGraphCheckpointModel
        from sqlalchemy.dialects.postgresql import insert
        import base64
        
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]
        
        chk_type, chk_bytes = self.serde.dumps_typed(checkpoint)
        meta_type, meta_bytes = self.serde.dumps_typed(metadata)
        
        async with self.session_maker() as db:
            stmt = insert(LangGraphCheckpointModel).values(
                thread_id=thread_id,
                checkpoint_id=checkpoint_id,
                parent_checkpoint_id=config["configurable"].get("checkpoint_id"),
                checkpoint_payload={
                    "type": chk_type,
                    "payload": base64.b64encode(chk_bytes).decode("ascii")
                },
                metadata_payload={
                    "type": meta_type,
                    "payload": base64.b64encode(meta_bytes).decode("ascii")
                }
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['thread_id', 'checkpoint_id'],
                set_=dict(
                    checkpoint_payload=stmt.excluded.checkpoint_payload,
                    metadata_payload=stmt.excluded.metadata_payload
                )
            )
            await db.execute(stmt)
            await db.commit()
            
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint_id
            }
        }
        
    async def alist(self, config: dict, *, filter: dict = None, before: dict = None, limit: int = None) -> AsyncIterator[CheckpointTuple]:
        from sqlalchemy import select
        from src.infrastructure.database.models import LangGraphCheckpointModel
        import base64
        
        thread_id = config["configurable"]["thread_id"]
        
        async with self.session_maker() as db:
            stmt = select(LangGraphCheckpointModel).where(LangGraphCheckpointModel.thread_id == thread_id)
            
            stmt = stmt.order_by(LangGraphCheckpointModel.checkpoint_id.desc())
            if limit:
                stmt = stmt.limit(limit)
                
            result = await db.execute(stmt)
            records = result.scalars().all()
            
            for record in records:
                chk_type = record.checkpoint_payload.get("type", "json")
                chk_bytes = base64.b64decode(record.checkpoint_payload["payload"])
                checkpoint = self.serde.loads_typed((chk_type, chk_bytes))
                
                meta_type = record.metadata_payload.get("type", "json")
                meta_bytes = base64.b64decode(record.metadata_payload["payload"])
                metadata = self.serde.loads_typed((meta_type, meta_bytes))
                
                yield CheckpointTuple(
                    config={"configurable": {"thread_id": record.thread_id, "checkpoint_id": record.checkpoint_id}},
                    checkpoint=checkpoint,
                    metadata=metadata,
                    parent_config={"configurable": {"thread_id": record.thread_id, "checkpoint_id": record.parent_checkpoint_id}} if record.parent_checkpoint_id else None
                )
