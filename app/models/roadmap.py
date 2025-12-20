from pydantic import BaseModel
from typing import List


class RoadmapItem(BaseModel):
    week: int
    skill: str
    objectives: List[str]
    resources: List[str]
    project_idea: str


class Roadmap(BaseModel):
    user_id: str
    target_role: str
    items: List[RoadmapItem]
