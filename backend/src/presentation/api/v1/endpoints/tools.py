from fastapi import APIRouter
from src.presentation.api.dependencies.auth import get_current_user
from src.infrastructure.database.models import UserModel
, Depends
from typing import Dict, Any
from uuid import UUID

router = APIRouter()

@router.post("/discover")
async def discover_tools(current_user: UserModel = Depends(get_current_user), ) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

from fastapi import HTTPException

@router.post("/{tool_id}/execute")
async def execute_tool(current_user: UserModel = Depends(get_current_user), tool_id: str, request: Dict[str, Any]) -> Any:
    # Manual tool execution API is not yet available; tools must be executed via the Agent Runtime.
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/providers")
async def list_providers() -> Any:
    return []

@router.get("/health")
async def check_health() -> Any:
    return {"status": "healthy"}

@router.get("/capabilities")
async def list_capabilities() -> Any:
    return []

@router.post("/cache/invalidate")
async def invalidate_cache(current_user: UserModel = Depends(get_current_user), ) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")
