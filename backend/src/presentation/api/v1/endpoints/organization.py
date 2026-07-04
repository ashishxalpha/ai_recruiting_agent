from fastapi import APIRouter
from src.presentation.api.dependencies.auth import get_current_user
from src.infrastructure.database.models import UserModel
, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from uuid import UUID

from src.presentation.api.dependencies import get_db_session
from src.application.schemas.common import StandardResponseDTO
from src.application.schemas.organization import (
    OrganizationGoalDTO, OrganizationRoleDTO, OrganizationSkillDTO,
    OrganizationExecutionDTO, OrganizationPolicyDTO, OrganizationLearningDTO,
    OrganizationMetricDTO, OrganizationActivityDTO
)
from src.application.services.organization.organization_query_service import OrganizationQueryService

router = APIRouter()

def get_org_service(db: AsyncSession = Depends(get_db_session)) -> OrganizationQueryService:
    return OrganizationQueryService(db)

@router.get("", response_model=StandardResponseDTO[dict])
async def get_organization(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_overview()

@router.get("/goals", response_model=StandardResponseDTO[List[OrganizationGoalDTO]])
async def list_goals(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_goals()

@router.get("/roles", response_model=StandardResponseDTO[List[OrganizationRoleDTO]])
async def list_roles(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_roles()

@router.get("/skills", response_model=StandardResponseDTO[List[OrganizationSkillDTO]])
async def list_skills(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_skills()

@router.get("/executions", response_model=StandardResponseDTO[List[OrganizationExecutionDTO]])
async def list_executions(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_executions()

@router.get("/policies", response_model=StandardResponseDTO[List[OrganizationPolicyDTO]])
async def get_policies(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_policies()

@router.get("/learning", response_model=StandardResponseDTO[List[OrganizationLearningDTO]])
async def get_learning(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_learning()

@router.get("/metrics", response_model=StandardResponseDTO[List[OrganizationMetricDTO]])
async def get_metrics(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_metrics()

@router.get("/activity", response_model=StandardResponseDTO[List[OrganizationActivityDTO]])
async def get_activity(service: OrganizationQueryService = Depends(get_org_service)):
    return await service.get_activity()

# Kept for compatibility / write ops
@router.post("/goals")
async def create_goal(current_user: UserModel = Depends(get_current_user), request: Dict[str, Any]) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/skills/{skill_id}/execute")
async def execute_skill(current_user: UserModel = Depends(get_current_user), skill_id: UUID, payload: Dict[str, Any]) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")
