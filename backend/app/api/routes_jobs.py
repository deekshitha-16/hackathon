from fastapi import APIRouter
from typing import List
from app.models.job import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/mock", response_model=List[Job])
def get_mock_jobs():
    return [
        Job(
            id="job_1",
            title="Data Scientist",
            company="Coffee Beans Consulting",
            location="Bangalore, India",
            link="https://example.com/jobs/ds-1",
            required_skills=["Python", "Machine Learning", "SQL", "Pandas"],
            match_score=78,
        ),
        Job(
            id="job_2",
            title="ML Engineer",
            company="Product Startup",
            location="Remote",
            link="https://example.com/jobs/ml-1",
            required_skills=["Python", "Deep Learning", "MLOps"],
            match_score=65,
        ),
    ]
