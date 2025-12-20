from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_profile import router as profile_router
from app.api.routes_roadmap import router as roadmap_router
from app.api.routes_jobs import router as jobs_router
from app.api.routes_interview import router as interview_router

from app.db.session import engine
from app.db.base import Base


app = FastAPI(title="CareerPilot API")
Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(profile_router)
app.include_router(roadmap_router)
app.include_router(jobs_router)
app.include_router(interview_router)


@app.get("/")
def read_root():
    return {"message": "CareerPilot backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
