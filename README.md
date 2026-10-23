# CareerMatch AI — GenAI Job Recommendation Platform

An independently implemented, production-oriented AI job recommendation platform combining hybrid matching, explainable scoring, optional LLM summaries, FastAPI, browser UI, and MCP tool integration.

> Original implementation inspired only by the high-level problem domain. It is not a copy of any third-party repository.

## Features
- Hybrid ranking: text similarity + skills + role + experience + location
- Explainable match scores and skill gaps
- Optional OpenAI career summary
- MCP tools: search jobs, get job, recommend jobs, skill-gap analysis
- FastAPI REST API + Swagger
- Browser UI
- Synthetic local job dataset for reproducible demos
- Tests
- No Docker

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and optionally add an OpenAI key.

Start:

```bash
uvicorn app:app --reload --port 8080
```

Open `http://127.0.0.1:8080`

Swagger: `http://127.0.0.1:8080/docs`

Health: `http://127.0.0.1:8080/health`

## MCP server

```bash
python mcp_server.py
```

MCP tools:
- `search_jobs`
- `get_job`
- `recommend_jobs`
- `skill_gap_analysis`

## Architecture

```text
Candidate Profile
      |
      v
Profile Normalizer
      |
      v
Hybrid Recommendation Engine
(TF-IDF + Skills + Role + Experience + Location)
      |
      +----> Ranked Jobs + Explainability
      |
      +----> Skill Gap Analysis
      |
      +----> Optional LLM Summary
      |
      +----> FastAPI / Browser UI
      |
      +----> MCP Tools
```

## Scoring

`final_score = 0.40 text + 0.30 skills + 0.15 role + 0.10 experience + 0.05 location`

The included jobs are synthetic demo records. No credentials or private candidate information are included.
