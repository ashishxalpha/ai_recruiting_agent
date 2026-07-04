from fastapi import APIRouter
from src.presentation.api.dependencies.auth import get_current_user
from src.infrastructure.database.models import UserModel
, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from uuid import UUID

from src.presentation.api.dependencies import get_db_session
from src.application.schemas.common import StandardResponseDTO
from src.application.schemas.agent import (
    AgentRuntimeDTO, AgentSessionDTO, AgentThoughtDTO,
    AgentActionDTO, AgentToolDTO, AgentMemoryDTO,
    AgentReflectionDTO, AgentReplayDTO
)
from src.application.services.agents.agent_query_service import AgentQueryService

router = APIRouter()

def get_agent_service(db: AsyncSession = Depends(get_db_session)) -> AgentQueryService:
    return AgentQueryService(db)

@router.get("", response_model=StandardResponseDTO[List[Dict[str, Any]]])
async def list_agents(service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_overview()

@router.get("/{agent_id}/runtime", response_model=StandardResponseDTO[AgentRuntimeDTO])
async def get_agent_runtime(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_runtime(agent_id)

@router.get("/{agent_id}/sessions", response_model=StandardResponseDTO[List[AgentSessionDTO]])
async def get_agent_sessions(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_sessions(agent_id)

@router.get("/{agent_id}/thoughts", response_model=StandardResponseDTO[List[AgentThoughtDTO]])
async def get_agent_thoughts(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_thoughts(agent_id)

@router.get("/{agent_id}/actions", response_model=StandardResponseDTO[List[AgentActionDTO]])
async def get_agent_actions(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_actions(agent_id)

@router.get("/{agent_id}/tools", response_model=StandardResponseDTO[List[AgentToolDTO]])
async def get_agent_tools(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_tools(agent_id)

@router.get("/{agent_id}/memory", response_model=StandardResponseDTO[List[AgentMemoryDTO]])
async def get_agent_memory(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_memory(agent_id)

@router.get("/{agent_id}/reflection", response_model=StandardResponseDTO[List[AgentReflectionDTO]])
async def get_agent_reflection(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_reflection(agent_id)

@router.get("/{agent_id}/replay", response_model=StandardResponseDTO[AgentReplayDTO])
async def get_agent_replay(agent_id: str, service: AgentQueryService = Depends(get_agent_service)):
    return await service.get_replay(agent_id)

# Write operations kept for compatibility
@router.post("", response_model=StandardResponseDTO[Dict[str, Any]])
async def create_agent(current_user: UserModel = Depends(get_current_user), request: Dict[str, Any], db: AsyncSession = Depends(get_db_session)) -> Any:
    # In a full implementation, this calls AgentRuntime.create()
    return StandardResponseDTO(data={"id": "00000000-0000-0000-0000-000000000000", "status": "CREATED"})

@router.post("/{agent_id}/start", response_model=StandardResponseDTO[Dict[str, Any]])
async def start_agent(current_user: UserModel = Depends(get_current_user), agent_id: UUID, request: Dict[str, Any], db: AsyncSession = Depends(get_db_session)) -> Any:
    # In a full implementation, this calls AgentRuntime.start() and triggers the CognitivePipeline
    return StandardResponseDTO(data={"status": "RUNNING"})

@router.post("/{agent_id}/pause", response_model=StandardResponseDTO[Dict[str, Any]])
async def pause_agent(current_user: UserModel = Depends(get_current_user), agent_id: UUID, db: AsyncSession = Depends(get_db_session)) -> Any:
    return StandardResponseDTO(data={"status": "PAUSED"})

@router.post("/{agent_id}/resume", response_model=StandardResponseDTO[Dict[str, Any]])
async def resume_agent(current_user: UserModel = Depends(get_current_user), agent_id: UUID, db: AsyncSession = Depends(get_db_session)) -> Any:
    return StandardResponseDTO(data={"status": "RUNNING"})

@router.post("/{agent_id}/cancel", response_model=StandardResponseDTO[Dict[str, Any]])
async def cancel_agent(current_user: UserModel = Depends(get_current_user), agent_id: UUID, db: AsyncSession = Depends(get_db_session)) -> Any:
    return StandardResponseDTO(data={"status": "TERMINATED"})
