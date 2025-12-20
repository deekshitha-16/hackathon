from pydantic import BaseModel
from typing import List, Optional


class Skill(BaseModel):
    name: str
    level: int  # 1–5


class Experience(BaseModel):
    title: str
    company: str
    years: float


class Profile(BaseModel):
    id: str
    name: str
    headline: str
    target_role: str
    skills: List[Skill]
    experiences: List[Experience]
    readiness_score: int  # 0–100
