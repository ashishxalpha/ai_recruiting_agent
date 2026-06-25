from pydantic import BaseModel, Field
from typing import List

class ProfileEvaluationResult(BaseModel):
    confidence_score: float = Field(..., description="Overall confidence score of the extraction (0.0 to 1.0)")
    completeness_score: float = Field(..., description="Completeness score based on required fields (0.0 to 1.0)")
    quality_score: float = Field(..., description="Quality score of the extracted data (0.0 to 1.0)")
    warnings: List[str] = Field(default_factory=list, description="List of warnings (e.g., missing critical fields)")
    issues: List[str] = Field(default_factory=list, description="List of critical issues that might prevent Candidate creation")
    
    # Granular confidences
    contact_confidence: float = Field(0.0, description="Confidence in contact info extraction")
    education_confidence: float = Field(0.0, description="Confidence in education extraction")
    experience_confidence: float = Field(0.0, description="Confidence in experience extraction")
    skills_confidence: float = Field(0.0, description="Confidence in skills extraction")
