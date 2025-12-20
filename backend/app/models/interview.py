from pydantic import BaseModel
from typing import List


class InterviewQuestion(BaseModel):
    id: str
    question: str
    category: str  # "technical" or "behavioral"
    difficulty: int  # 1–5


class InterviewQuestionSet(BaseModel):
    role: str
    questions: List[InterviewQuestion]
