from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.application.services.workflows.providers import (
    SummaryProvider,
    GraphProvider,
    TimelineProvider,
    NodeProvider,
    EventProvider,
    CheckpointProvider,
    StatisticsProvider
)
from src.application.schemas.workflow import (
    WorkflowResponseDTO,
    WorkflowSummaryDTO,
    WorkflowGraphDTO,
    WorkflowTimelineDTO,
    WorkflowNodeHistoryDTO,
    WorkflowEventListDTO,
    WorkflowCheckpointListDTO,
    WorkflowStatisticsDTO
)

class WorkflowQueryService:
    """Orchestrator for Workflow Platform read models. Delegates to domain-specific providers."""
    
    def __init__(self, session: AsyncSession):
        self.summary_provider = SummaryProvider(session)
        self.graph_provider = GraphProvider(session)
        self.timeline_provider = TimelineProvider(session)
        self.node_provider = NodeProvider(session)
        self.event_provider = EventProvider(session)
        self.checkpoint_provider = CheckpointProvider(session)
        self.statistics_provider = StatisticsProvider(session)

    async def get_summary(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowSummaryDTO]:
        return await self.summary_provider.get_summary(workflow_id)

    async def get_list(self) -> WorkflowResponseDTO[list[WorkflowSummaryDTO]]:
        return await self.summary_provider.get_list()

    async def get_graph(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowGraphDTO]:
        return await self.graph_provider.get_graph(workflow_id)

    async def get_timeline(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowTimelineDTO]:
        return await self.timeline_provider.get_timeline(workflow_id)

    async def get_nodes(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowNodeHistoryDTO]:
        return await self.node_provider.get_nodes(workflow_id)

    async def get_events(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowEventListDTO]:
        return await self.event_provider.get_events(workflow_id)

    async def get_checkpoints(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowCheckpointListDTO]:
        return await self.checkpoint_provider.get_checkpoints(workflow_id)

    async def get_statistics(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowStatisticsDTO]:
        return await self.statistics_provider.get_statistics(workflow_id)
