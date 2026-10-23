from pathlib import Path
from careermatch.data import JobRepository
from careermatch.models import CandidateProfile
from careermatch.recommender import JobRecommender

def test_recommendation_returns_ranked_jobs():
    root = Path(__file__).resolve().parents[1]
    engine = JobRecommender(JobRepository(root / "data" / "jobs.csv"))
    p = CandidateProfile(name="Test", skills=["Python","LangGraph","RAG","FastAPI","OpenAI"], experience_years=3, target_role="AI Engineer", location="Pune", top_k=3)
    r = engine.recommend(p)
    assert len(r) == 3
    assert r[0]["match_score"] >= r[1]["match_score"]
    assert "matched_skills" in r[0]
