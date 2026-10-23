from pathlib import Path
import pandas as pd

class JobRepository:
    def __init__(self, path: Path):
        self.df = pd.read_csv(path).fillna("")

    def records(self):
        return self.df.to_dict(orient="records")

    def get(self, job_id):
        rows = self.df[self.df["job_id"].astype(str) == str(job_id)]
        return None if rows.empty else rows.iloc[0].to_dict()

    def search(self, query="", limit=20):
        limit = max(1, min(int(limit), 100))
        if not query.strip():
            return self.records()[:limit]
        q = query.lower()
        cols = ["title", "company", "location", "skills", "description"]
        mask = self.df[cols].astype(str).apply(
            lambda c: c.str.lower().str.contains(q, regex=False)
        ).any(axis=1)
        return self.df[mask].head(limit).to_dict(orient="records")
