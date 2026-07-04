import asyncio
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import insert
from sqlalchemy.pool import NullPool

from src.infrastructure.events.event_bus import EventBus
from src.infrastructure.tools.pipeline import ToolExecutionCompleted
from src.infrastructure.database.models import ToolExecutionModel

logger = logging.getLogger(__name__)

class ExecutionRecorder:
    def __init__(self, async_session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = async_session_maker

    async def handle_tool_execution_completed(self, event: ToolExecutionCompleted):
        # We record the event without blocking the main workflow
        # Note: If this fails, we log it and suppress the error so the workflow continues
        try:
            async with self.session_maker() as session:
                stmt = insert(ToolExecutionModel).values(
                    id=event.execution_id, # execution_id could be unique per attempt or we could use event_id
                    workflow_id=event.workflow_id,
                    agent_id=event.agent_id,
                    trace_id=event.trace_id,
                    provider=event.provider_id,
                    tool=event.tool_id,
                    operation=event.operation,
                    status=event.status,
                    latency_ms=event.latency_ms,
                    error_details=event.error,
                    retry_count=event.retry_count,
                    started_at=event.occurred_at,
                    completed_at=event.occurred_at
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.error(f"Failed to record ToolExecutionCompleted for execution {event.execution_id}: {e}")
            # Do NOT re-raise
            # Monitoring system would pick up this error log

    def start(self):
        self.queue = EventBus.subscribe()
        asyncio.create_task(self._process_events())

    async def _process_events(self):
        while True:
            try:
                event = await self.queue.get()
                if isinstance(event, ToolExecutionCompleted):
                    await self.handle_tool_execution_completed(event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing event: {e}")
