from fastapi import APIRouter
from app.models.interview import InterviewQuestion, InterviewQuestionSet

router = APIRouter(prefix="/interview", tags=["interview"])


@router.get("/mock_questions", response_model=InterviewQuestionSet)
def get_mock_questions():
    questions = [
        InterviewQuestion(
            id="q1",
            question="Explain the difference between supervised and unsupervised learning with examples.",
            category="technical",
            difficulty=2,
        ),
        InterviewQuestion(
            id="q2",
            question="How would you evaluate a classification model beyond accuracy?",
            category="technical",
            difficulty=3,
        ),
        InterviewQuestion(
            id="q3",
            question="Tell me about a time you handled an ambiguous problem in a project.",
            category="behavioral",
            difficulty=2,
        ),
    ]

    return InterviewQuestionSet(
        role="Data Scientist",
        questions=questions,
    )
