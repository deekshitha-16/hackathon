from pydantic import BaseModel
from typing import List


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    link: str
    required_skills: List[str]
    match_score: int  # 0–100
