from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date

class Education(BaseModel):
    institution: str = Field(..., description="Name of the educational institution")
    degree: Optional[str] = Field(None, description="Degree obtained or being pursued")
    field_of_study: Optional[str] = Field(None, description="Major or field of study")
    start_date: Optional[date] = Field(None, description="Start date (YYYY-MM-DD format if known)")
    end_date: Optional[date] = Field(None, description="End date (YYYY-MM-DD format if known)")
    description: Optional[str] = Field(None, description="Additional details about the education")

class Experience(BaseModel):
    company: str = Field(..., description="Name of the company or organization")
    title: str = Field(..., description="Job title or role")
    start_date: Optional[date] = Field(None, description="Start date (YYYY-MM-DD format if known)")
    end_date: Optional[date] = Field(None, description="End date (YYYY-MM-DD format if known)")
    description: Optional[str] = Field(None, description="Description of responsibilities and achievements")

class Project(BaseModel):
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(None, description="Description of the project and candidate's role")
    url: Optional[str] = Field(None, description="Link to the project if available")

class Skill(BaseModel):
    name: str = Field(..., description="Name of the skill (e.g., Python, React, Project Management)")
    proficiency: Optional[str] = Field(None, description="Proficiency level if mentioned (e.g., Beginner, Intermediate, Expert)")

class Certification(BaseModel):
    name: str = Field(..., description="Name of the certification")
    issuer: Optional[str] = Field(None, description="Issuing organization")
    date_issued: Optional[date] = Field(None, description="Date the certification was issued")

class Language(BaseModel):
    name: str = Field(..., description="Name of the language")
    proficiency: Optional[str] = Field(None, description="Proficiency level (e.g., Native, Fluent, Conversational)")

class CandidateProfile(BaseModel):
    first_name: Optional[str] = Field(None, description="Candidate's first name")
    last_name: Optional[str] = Field(None, description="Candidate's last name")
    email: Optional[EmailStr] = Field(None, description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    
    education: List[Education] = Field(default_factory=list, description="List of educational qualifications")
    experience: List[Experience] = Field(default_factory=list, description="List of work experiences")
    projects: List[Project] = Field(default_factory=list, description="List of significant projects")
    skills: List[Skill] = Field(default_factory=list, description="List of skills")
    certifications: List[Certification] = Field(default_factory=list, description="List of certifications")
    languages: List[Language] = Field(default_factory=list, description="List of spoken languages")
