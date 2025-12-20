from fastapi import APIRouter
from app.models.roadmap import Roadmap, RoadmapItem

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.get("/mock", response_model=Roadmap)
def get_mock_roadmap():
    items = [
        RoadmapItem(
            week=1,
            skill="Python for Data Science",
            objectives=[
                "Revise Python basics (lists, dicts, functions)",
                "Learn NumPy fundamentals",
                "Practice pandas for data manipulation",
            ],
            resources=[
                "https://docs.python.org/3/tutorial/",
                "https://numpy.org/devdocs/user/quickstart.html",
                "https://pandas.pydata.org/docs/getting_started/index.html",
            ],
            project_idea="Analyze a small CSV dataset and create summary stats.",
        ),
        RoadmapItem(
            week=2,
            skill="Machine Learning Fundamentals",
            objectives=[
                "Understand supervised vs unsupervised learning",
                "Learn linear regression and logistic regression",
                "Implement models using scikit-learn",
            ],
            resources=[
                "https://scikit-learn.org/stable/user_guide.html",
                "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
            ],
            project_idea="Build a model to predict something like house prices or churn.",
        ),
    ]

    return Roadmap(
        user_id="user_1",
        target_role="Data Scientist",
        items=items,
    )
