from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Union

class QueryRequest(BaseModel):
    prompt: str
    n_results: Optional[int] = None

class WorkExperience(BaseModel):
    job_title: str = Field(default="Not Specified")
    company: str = Field(default="Not Specified")
    period: Optional[str] = Field(default=None, description="Ej: 2018-2020 o Jan 2015 to Present")
    description: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)

class Education(BaseModel):
    degree: str = Field(default="Not Specified")
    institution: str = Field(default="Not Specified")
    year: Optional[Union[int, str]] = Field(default=None)

class Certification(BaseModel):
    name: str = Field(default="Not Specified")
    year: Optional[Union[int, str]] = Field(default=None)

class Structured_CV(BaseModel):
    full_name: str = Field(default="Candidate Name")
    summary: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    tech_stack: List[str] = Field(default_factory=list)
    work_history: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    english_level: str = Field(default="Not specified")
    matchmaking_summary: str = Field(
        default="Summary not generated.", 
        description="A paragraph for semantic search."
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def ensure_name(cls, v: Any) -> str:
        return str(v) if v else "Candidate Name"