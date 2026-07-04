from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, Any

T = TypeVar("T")

class ResponseMetadataDTO(BaseModel):
    feature_available: bool
    data_available: bool
    message: Optional[str] = None

class StandardResponseDTO(BaseModel, Generic[T]):
    """Standardized envelope for all Frontend Integration Phase 2 responses."""
    data: Optional[T] = None
    metadata: ResponseMetadataDTO

def create_response(data: Optional[T], feature_available: bool = True, data_available: bool = True, message: Optional[str] = None) -> StandardResponseDTO[T]:
    return StandardResponseDTO(
        data=data,
        metadata=ResponseMetadataDTO(
            feature_available=feature_available,
            data_available=data_available,
            message=message
        )
    )
