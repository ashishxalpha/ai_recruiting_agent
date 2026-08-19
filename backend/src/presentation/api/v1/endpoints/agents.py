from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.presentation.api.dependencies import get_db_session
from src.infrastructure.database.models import WorkflowExecutionModel, WorkflowEventModel

router = APIRouter()

STATIC_AGENTS = [
    {
        "id": "00000000-0000-0000-0000-000000000000",
        "name": "Core Recruiting Agent",
        "description": "Orchestrates candidate evaluation and extraction.",
        "status": "READY"
    }
]

@router.post("")
async def create_agent(request: Dict[str, Any], db: AsyncSession = Depends(get_db_session)) -> Any:
    return {"id": STATIC_AGENTS[0]["id"], "status": "CREATED"}

@router.get("")
async def list_agents() -> List[Dict[str, Any]]:
    return STATIC_AGENTS

@router.post("/{agent_id}/start")
async def start_agent(agent_id: UUID, request: Dict[str, Any], db: AsyncSession = Depends(get_db_session)) -> Any:
    return {"status": "RUNNING"}

@router.post("/{agent_id}/pause")
async def pause_agent(agent_id: UUID) -> Any:
    return {"status": "PAUSED"}

@router.post("/{agent_id}/resume")
async def resume_agent(agent_id: UUID) -> Any:
    return {"status": "RUNNING"}

@router.post("/{agent_id}/cancel")
async def cancel_agent(agent_id: UUID) -> Any:
    return {"status": "TERMINATED"}

@router.get("/{agent_id}")
async def get_agent(agent_id: UUID) -> Any:
    return STATIC_AGENTS[0]

@router.get("/{agent_id}/sessions")
async def get_agent_sessions(agent_id: UUID, db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    stmt = select(WorkflowExecutionModel).order_by(WorkflowExecutionModel.started_at.desc()).limit(10)
    result = await db.execute(stmt)
    executions = result.scalars().all()
    
    return [
        {
            "id": str(ex.id),
            "status": ex.status,
            "started_at": ex.started_at.isoformat() if ex.started_at else None,
            "completed_at": ex.completed_at.isoformat() if ex.completed_at else None
        }
        for ex in executions
    ]

@router.get("/{agent_id}/history")
async def get_agent_history(agent_id: UUID) -> List[Dict[str, Any]]:
    return []

@router.get("/{agent_id}/events")
async def get_agent_events(agent_id: UUID, db: AsyncSession = Depends(get_db_session)) -> List[Dict[str, Any]]:
    stmt = select(WorkflowEventModel).order_by(WorkflowEventModel.timestamp.desc()).limit(50)
    result = await db.execute(stmt)
    events = result.scalars().all()
    
    return [
        {
            "id": str(ev.id),
            "category": ev.category,
            "message": ev.message,
            "severity": ev.severity,
            "timestamp": ev.timestamp.isoformat() if ev.timestamp else None
        }
        for ev in events
    ]

@router.get("/{agent_id}/replay")
async def replay_agent_session(agent_id: UUID, session_id: UUID) -> List[Dict[str, Any]]:
    return []
