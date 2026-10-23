import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def norm(x):
    return re.sub(r"\s+", " ", str(x).strip().lower())

def skills(values):
    return {norm(x) for x in values if str(x).strip()}

def parse_skills(raw):
    return skills(re.split(r"[,;|]", raw or ""))

def similarity(a, b):
    if not str(a).strip() or not str(b).strip():
        return 0.0
    v = TfidfVectorizer(stop_words="english")
    m = v.fit_transform([str(a), str(b)])
    return float(cosine_similarity(m[0:1], m[1:2])[0][0])

def overlap(candidate, required):
    c, r = skills(candidate), skills(required)
    if not r:
        return 0.0, set(), set()
    matched, missing = c & r, r - c
    return len(matched) / len(r), matched, missing

def experience_score(candidate, minimum):
    minimum = float(minimum or 0)
    return 1.0 if minimum <= 0 else min(1.0, max(0.0, candidate / minimum))

def location_score(candidate, job, remote):
    if remote and "remote" in str(job).lower():
        return 1.0
    if candidate and candidate.lower() in str(job).lower():
        return 1.0
    return 0.5 if not candidate else 0.0
