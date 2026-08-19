from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class IngestionItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    filename: str
    status: str
    created_at: datetime
    candidate_id: Optional[UUID] = None
    error_message: Optional[str] = None
