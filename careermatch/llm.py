from .config import OPENAI_API_KEY, OPENAI_MODEL

def generate_career_summary(profile, recommendations):
    if not OPENAI_API_KEY:
        return "LLM summary unavailable; deterministic ranking remains fully functional."
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    jobs = [{"title":r["job"]["title"],"company":r["job"]["company"],
             "score":r["match_score"],"matched":r["matched_skills"],
             "missing":r["missing_skills"]} for r in recommendations]
    prompt = ("Give a concise career recommendation using only these facts. "
              "Mention the best-fit role, strongest skills and 2-3 skill gaps. "
              f"Profile: {profile}\nRanked jobs: {jobs}")
    res = client.chat.completions.create(
        model=OPENAI_MODEL, temperature=0.2,
        messages=[{"role":"system","content":"Be factual and concise."},
                  {"role":"user","content":prompt}]
    )
    return res.choices[0].message.content.strip()
