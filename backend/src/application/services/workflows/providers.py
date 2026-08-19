from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
import uuid
from typing import Dict, Any
from datetime import datetime, timedelta

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
    WorkflowGraphEdgeDTO,
    WorkflowTimelineEntryDTO,
    WorkflowNodeExecutionDTO,
    WorkflowEventDTO,
    WorkflowCheckpointDTO
)
from src.infrastructure.database.models import (
    WorkflowExecutionModel,
    WorkflowNodeExecutionModel,
    WorkflowEventModel,
    LangGraphCheckpointModel
)

class SummaryProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_summary(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowSummaryDTO]:
        result = await self.session.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        
        if not execution:
            return WorkflowResponseDTO(status="unavailable", error="Workflow execution not found")
            
        return WorkflowResponseDTO(
            status="available",
            data=WorkflowSummaryDTO(
                id=execution.id,
                job_id=execution.job_id or uuid.uuid4(),
                candidate_id=execution.candidate_id or uuid.uuid4(),
                status=execution.status,
                started_at=execution.started_at,
                current_node=execution.current_node or "",
                workflow_version=execution.workflow_version
            )
        )

    async def get_list(self) -> WorkflowResponseDTO[list[WorkflowSummaryDTO]]:
        result = await self.session.execute(
            select(WorkflowExecutionModel)
            .order_by(WorkflowExecutionModel.started_at.desc())
            .limit(20)
        )
        executions = result.scalars().all()
        
        dtos = []
        for execution in executions:
            dtos.append(
                WorkflowSummaryDTO(
                    id=execution.id,
                    job_id=execution.job_id or uuid.uuid4(),
                    candidate_id=execution.candidate_id or uuid.uuid4(),
                    status=execution.status,
                    started_at=execution.started_at,
                    current_node=execution.current_node or "",
                    workflow_version=execution.workflow_version
                )
            )
            
        return WorkflowResponseDTO(status="available", data=dtos)

class GraphProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_graph(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowGraphDTO]:
        result = await self.session.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        if not execution:
            return WorkflowResponseDTO(status="unavailable", error="Workflow execution not found")
            
        current_node = execution.current_node
        
        # Get all executed nodes in order
        nodes_result = await self.session.execute(
            select(WorkflowNodeExecutionModel)
            .where(WorkflowNodeExecutionModel.workflow_execution_id == workflow_id)
            .order_by(WorkflowNodeExecutionModel.start_time.asc())
        )
        executed_nodes = nodes_result.scalars().all()
        
        if not executed_nodes:
            # Fallback to empty if no nodes executed yet
            return WorkflowResponseDTO(status="available", data=WorkflowGraphDTO(
                nodes=[], edges=[], current_node_id=current_node
            ))
            
        unique_nodes = []
        seen = set()
        for n in executed_nodes:
            if n.node_id not in seen:
                seen.add(n.node_id)
                unique_nodes.append(n.node_id)
                
        # Build node DTOs
        nodes = []
        y_offset = 0
        for i, nid in enumerate(unique_nodes):
            nodes.append(
                WorkflowGraphNodeDTO(
                    id=nid,
                    type="default",
                    data={"label": nid.replace("_", " ").title()},
                    position={"x": 250, "y": y_offset}
                )
            )
            y_offset += 100
            
        # Build edge DTOs
        edges = []
        for i in range(len(unique_nodes) - 1):
            source = unique_nodes[i]
            target = unique_nodes[i+1]
            edges.append(
                WorkflowGraphEdgeDTO(
                    id=f"e{i}",
                    source=source,
                    target=target
                )
            )
            
        data = WorkflowGraphDTO(
            nodes=nodes,
            edges=edges,
            current_node_id=current_node
        )
        return WorkflowResponseDTO(status="available", data=data)

class TimelineProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_timeline(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowTimelineDTO]:
        result = await self.session.execute(
            select(WorkflowEventModel)
            .where(WorkflowEventModel.workflow_execution_id == workflow_id)
            .order_by(WorkflowEventModel.timestamp.asc())
        )
        events = result.scalars().all()
        
        entries = []
        for evt in events:
            entries.append(
                WorkflowTimelineEntryDTO(
                    event_id=evt.id,
                    workflow_id=workflow_id,
                    timestamp=evt.timestamp,
                    state=evt.message,
                    node_id=evt.node_id,
                    metadata=evt.metadata_payload
                )
            )
            
        return WorkflowResponseDTO(status="available", data=WorkflowTimelineDTO(entries=entries))

class NodeProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_nodes(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowNodeHistoryDTO]:
        result = await self.session.execute(
            select(WorkflowNodeExecutionModel)
            .where(WorkflowNodeExecutionModel.workflow_execution_id == workflow_id)
            .order_by(WorkflowNodeExecutionModel.start_time.asc())
        )
        nodes = result.scalars().all()
        
        executions = []
        for n in nodes:
            executions.append(
                WorkflowNodeExecutionDTO(
                    node_id=n.node_id,
                    status=n.status,
                    start_time=n.start_time,
                    end_time=n.end_time,
                    duration_ms=n.duration_ms,
                    inputs=n.inputs,
                    outputs=n.outputs,
                    error_message=n.error_message,
                    tool_invocations=n.tool_invocations
                )
            )
            
        return WorkflowResponseDTO(status="available", data=WorkflowNodeHistoryDTO(executions=executions))

class EventProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_events(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowEventListDTO]:
        result = await self.session.execute(
            select(WorkflowEventModel)
            .where(WorkflowEventModel.workflow_execution_id == workflow_id)
            .order_by(WorkflowEventModel.timestamp.desc())
        )
        events = result.scalars().all()
        
        dtos = []
        for evt in events:
            dtos.append(
                WorkflowEventDTO(
                    event_id=evt.id,
                    timestamp=evt.timestamp,
                    category=evt.category,
                    severity=evt.severity,
                    message=evt.message,
                    node_id=evt.node_id
                )
            )
            
        return WorkflowResponseDTO(status="available", data=WorkflowEventListDTO(events=dtos))

class CheckpointProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_checkpoints(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowCheckpointListDTO]:
        exec_result = await self.session.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = exec_result.scalar_one_or_none()
        
        if not execution:
            return WorkflowResponseDTO(status="unavailable", error="Workflow not found")
            
        chk_result = await self.session.execute(
            select(LangGraphCheckpointModel)
            .where(LangGraphCheckpointModel.thread_id == execution.thread_id)
            .order_by(LangGraphCheckpointModel.created_at.desc())
        )
        checkpoints = chk_result.scalars().all()
        
        dtos = []
        for chk in checkpoints:
            dtos.append(
                WorkflowCheckpointDTO(
                    checkpoint_id=chk.checkpoint_id,
                    created_at=chk.created_at,
                    rollback_available=True,
                    workflow_version=execution.workflow_version,
                    state_snapshot={"keys": list(chk.checkpoint_payload.get("channel_values", {}).keys())} if chk.checkpoint_payload else {}
                )
            )
            
        return WorkflowResponseDTO(status="available", data=WorkflowCheckpointListDTO(checkpoints=dtos))

class StatisticsProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_statistics(self, workflow_id: UUID) -> WorkflowResponseDTO[WorkflowStatisticsDTO]:
        result = await self.session.execute(
            select(
                func.sum(WorkflowNodeExecutionModel.duration_ms),
                func.avg(WorkflowNodeExecutionModel.duration_ms),
                func.sum(WorkflowNodeExecutionModel.retries),
                func.sum(WorkflowNodeExecutionModel.tool_invocations),
                func.count(WorkflowNodeExecutionModel.id)
            )
            .where(WorkflowNodeExecutionModel.workflow_execution_id == workflow_id)
        )
        row = result.fetchone()
        
        total_duration = row[0] or 0.0
        avg_duration = row[1] or 0.0
        retries = row[2] or 0
        tools = row[3] or 0
        node_count = row[4] or 0
        
        return WorkflowResponseDTO(
            status="available",
            data=WorkflowStatisticsDTO(
                total_duration_ms=total_duration,
                average_node_time_ms=avg_duration,
                retries=retries,
                failures=0,
                human_approvals=0,
                checkpoint_count=0,
                tool_calls=tools,
                memory_retrievals=0
            )
        )
