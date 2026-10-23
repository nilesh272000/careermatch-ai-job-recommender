from pathlib import Path
from mcp.server.fastmcp import FastMCP
from careermatch.data import JobRepository
from careermatch.models import CandidateProfile
from careermatch.recommender import JobRecommender

BASE = Path(__file__).resolve().parent
repo = JobRepository(BASE / "data" / "jobs.csv")
engine = JobRecommender(repo)
mcp = FastMCP("CareerMatch AI")

@mcp.tool()
def search_jobs(query: str = "", limit: int = 10) -> list[dict]:
    return repo.search(query, limit)

@mcp.tool()
def get_job(job_id: str) -> dict:
    return repo.get(job_id) or {"error": "Job not found"}

@mcp.tool()
def recommend_jobs(name: str, skills: list[str], experience_years: float,
                   target_role: str = "", location: str = "",
                   remote_preference: bool = True, top_k: int = 5) -> list[dict]:
    profile = CandidateProfile(name=name, skills=skills, experience_years=experience_years,
                               target_role=target_role, location=location,
                               remote_preference=remote_preference, top_k=top_k)
    return engine.recommend(profile)

@mcp.tool()
def skill_gap_analysis(skills: list[str], target_role: str = "",
                       experience_years: float = 0) -> dict:
    profile = CandidateProfile(name="MCP Candidate", skills=skills,
                               experience_years=experience_years, target_role=target_role)
    return engine.skill_gap(profile)

if __name__ == "__main__":
    mcp.run(transport="stdio")
