from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Dict, Any

from src.application.schemas.workflow import (
    WorkflowResponseDTO,
    WorkflowSummaryDTO,
    WorkflowGraphDTO,
    WorkflowTimelineDTO,
    WorkflowNodeHistoryDTO,
    WorkflowEventListDTO,
    WorkflowCheckpointListDTO,
    WorkflowStatisticsDTO,
    WorkflowGraphNodeDTO,
    WorkflowGraphEdgeDTO
)

class SummaryProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_summary(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowSummaryDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="Workflow summary persistence not fully integrated."
        )

class GraphProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_graph(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowGraphDTO]:
        # Return a static default topology to unblock React Flow rendering
        data = WorkflowGraphDTO(
            nodes=[
                WorkflowGraphNodeDTO(id="upload", type="default", data={"label": "Upload Validation"}, position={"x": 250, "y": 0}),
                WorkflowGraphNodeDTO(id="parse", type="default", data={"label": "Document Parsing"}, position={"x": 250, "y": 100}),
                WorkflowGraphNodeDTO(id="extract", type="default", data={"label": "AI Extraction"}, position={"x": 250, "y": 200}),
                WorkflowGraphNodeDTO(id="evaluate", type="default", data={"label": "Profile Evaluation"}, position={"x": 250, "y": 300}),
            ],
            edges=[
                WorkflowGraphEdgeDTO(id="e1", source="upload", target="parse"),
                WorkflowGraphEdgeDTO(id="e2", source="parse", target="extract"),
                WorkflowGraphEdgeDTO(id="e3", source="extract", target="evaluate")
            ],
            current_node_id="extract"
        )
        return WorkflowResponseDTO(status="available", data=data)

class TimelineProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_timeline(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowTimelineDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="Timeline event persistence not fully integrated."
        )

class NodeProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_nodes(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowNodeHistoryDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="Node execution history persistence not fully integrated."
        )

class EventProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_events(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowEventListDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="EventBus history persistence not fully integrated."
        )

class CheckpointProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_checkpoints(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowCheckpointListDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="LangGraph Checkpoint persistence not fully integrated."
        )

class StatisticsProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_statistics(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowStatisticsDTO]:
        return WorkflowResponseDTO(
            status="not_available",
            reason="Statistics aggregation persistence not fully integrated."
        )
