from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from careermatch.models import CandidateProfile
from careermatch.data import JobRepository
from careermatch.recommender import JobRecommender

BASE = Path(__file__).resolve().parent
app = FastAPI(title="CareerMatch AI", version="1.0.0")
templates = Jinja2Templates(directory=str(BASE / "templates"))
repository = JobRepository(BASE / "data" / "jobs.csv")
recommender = JobRecommender(repository)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok", "service": "careermatch-ai"}

@app.get("/jobs")
def jobs(query: str = "", limit: int = 20):
    return {"jobs": repository.search(query, limit)}

@app.post("/recommend")
def recommend(profile: CandidateProfile):
    return {"recommendations": recommender.recommend(profile)}

@app.post("/skill-gap")
def skill_gap(profile: CandidateProfile):
    return recommender.skill_gap(profile)
