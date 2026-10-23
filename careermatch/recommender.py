from .matching import parse_skills, overlap, similarity, experience_score, location_score
from .models import CandidateProfile

class JobRecommender:
    def __init__(self, repository):
        self.repository = repository

    def score(self, profile, job):
        required = parse_skills(job.get("skills", ""))
        skill_score, matched, missing = overlap(profile.skills, required)
        profile_text = " ".join(profile.skills) + " " + profile.target_role
        job_text = f"{job.get('title','')} {job.get('skills','')} {job.get('description','')}"
        text = similarity(profile_text, job_text)
        role = similarity(profile.target_role, job.get("title", ""))
        exp = experience_score(profile.experience_years, job.get("min_experience", 0))
        loc = location_score(profile.location, job.get("location", ""), profile.remote_preference)
        final = .40*text + .30*skill_score + .15*role + .10*exp + .05*loc
        return {
            "job": job,
            "match_score": round(final*100, 2),
            "signals": {"text_similarity": round(text*100,2),
                        "skill_match": round(skill_score*100,2),
                        "role_match": round(role*100,2),
                        "experience_match": round(exp*100,2),
                        "location_match": round(loc*100,2)},
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing)
        }

    def recommend(self, profile):
        ranked = [self.score(profile, j) for j in self.repository.records()]
        ranked.sort(key=lambda x: x["match_score"], reverse=True)
        for x in ranked:
            m = x["matched_skills"]
            g = x["missing_skills"]
            x["explanation"] = f"{x['match_score']}% match" + (
                f", strong overlap in {', '.join(m[:5])}." if m else "."
            ) + (f" Review skill gaps: {', '.join(g[:4])}." if g else " No major skill gaps detected.")
        return ranked[:profile.top_k]

    def skill_gap(self, profile):
        results = self.recommend(profile)
        counts = {}
        for r in results:
            for s in r["missing_skills"]:
                counts[s] = counts.get(s, 0) + 1
        ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return {"target_role": profile.target_role,
                "skills_to_develop": [s for s,_ in ordered[:10]],
                "evidence": [{"skill":s, "matched_jobs":n} for s,n in ordered[:10]]}
