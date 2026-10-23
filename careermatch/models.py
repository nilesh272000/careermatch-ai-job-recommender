from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str = "Candidate"
    skills: list[str] = Field(default_factory=list)
    experience_years: float = Field(default=0, ge=0)
    target_role: str = ""
    location: str = ""
    remote_preference: bool = True
    top_k: int = Field(default=5, ge=1, le=20)
