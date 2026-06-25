from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from uuid import UUID

router = APIRouter()

@router.post("")
async def create_agent(request: Dict[str, Any]) -> Any:
    return {"id": "00000000-0000-0000-0000-000000000000", "status": "CREATED"}

@router.get("")
async def list_agents() -> List[Dict[str, Any]]:
    return []

@router.post("/{agent_id}/start")
async def start_agent(agent_id: UUID, request: Dict[str, Any]) -> Any:
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
    return {"id": agent_id, "status": "READY"}

@router.get("/{agent_id}/sessions")
async def get_agent_sessions(agent_id: UUID) -> List[Dict[str, Any]]:
    return []

@router.get("/{agent_id}/history")
async def get_agent_history(agent_id: UUID) -> List[Dict[str, Any]]:
    return []

@router.get("/{agent_id}/events")
async def get_agent_events(agent_id: UUID) -> List[Dict[str, Any]]:
    return []

@router.get("/{agent_id}/replay")
async def replay_agent_session(agent_id: UUID, session_id: UUID) -> List[Dict[str, Any]]:
    return []
