"""Attach Git commit metadata to documents for richer retrieval."""
from datetime import datetime
import git
from config import cfg
PROJECT_DIR = cfg.PROJECT_DIR


def commit_messages(limit: int = 100):
    repo = git.Repo(str(PROJECT_DIR))
    for c in repo.iter_commits(max_count=limit):
        yield {
            "commit": c.hexsha,
            "author": c.author.name,
            "date": datetime.utcfromtimestamp(c.committed_date).isoformat(),
            "message": c.message.strip(),
        }