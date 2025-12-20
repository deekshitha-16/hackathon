from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.models.profile import Profile, Skill, Experience
from app.core.scoring import compute_readiness_score_from_skills
from app.services.profile_ingestion import save_resume_file
from app.utils.db_dependency import get_db
from app.models.db_models import User, ProfileDB, SkillDB, ExperienceDB
from app.utils.resume_parser import parse_resume_pdf

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/current", response_model=Profile)
def get_current_profile(db: Session = Depends(get_db)):
    """
    Return the latest profile for the demo user.
    This is what the Streamlit Dashboard uses.
    """
    user = db.query(User).filter(User.email == "demo@careerpilot.ai").first()
    if not user:
        raise RuntimeError("No profile found. Upload a resume first.")

    profile_db = (
        db.query(ProfileDB)
        .filter(ProfileDB.user_id == user.id)
        .order_by(ProfileDB.id.desc())
        .first()
    )
    if not profile_db:
        raise RuntimeError("No profile found. Upload a resume first.")

    skills_out = [Skill(name=s.name, level=s.level) for s in profile_db.skills]
    experiences_out = [
        Experience(title=e.title, company=e.company, years=e.years)
        for e in profile_db.experiences
    ]

    return Profile(
        id=str(profile_db.id),
        name=user.name,
        headline=profile_db.headline,
        target_role=profile_db.target_role,
        skills=skills_out,
        experiences=experiences_out,
        readiness_score=profile_db.readiness_score,
    )


@router.get("/score")
def get_score(target_role: str = "Data Scientist", db: Session = Depends(get_db)):
    """
    Compute readiness score for the current profile + target role,
    based on skills stored in the DB.
    """
    user = db.query(User).filter(User.email == "demo@careerpilot.ai").first()
    if not user:
        return {"target_role": target_role, "score": 10}

    profile_db = (
        db.query(ProfileDB)
        .filter(ProfileDB.user_id == user.id)
        .order_by(ProfileDB.id.desc())
        .first()
    )
    if not profile_db:
        return {"target_role": target_role, "score": 10}

    skill_tuples = [(s.name, s.level) for s in profile_db.skills]
    score = compute_readiness_score_from_skills(skill_tuples, target_role)

    profile_db.readiness_score = score
    profile_db.target_role = target_role
    db.commit()

    return {"target_role": target_role, "score": score}


@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Save the uploaded resume (PDF), parse it, and create a profile in the DB.
    """
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF resumes are supported for now."}

    content = await file.read()
    saved_path = save_resume_file(file.filename, content)

    parsed = parse_resume_pdf(saved_path)

    # get or create demo user
    user = db.query(User).filter(User.email == "demo@careerpilot.ai").first()
    if not user:
        user = User(name=parsed["name"], email="demo@careerpilot.ai")
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = parsed["name"]
        db.commit()

    target_role = "Data Scientist"  # default for now
    skill_tuples = parsed["skills"]
    readiness = compute_readiness_score_from_skills(skill_tuples, target_role)

    profile_db = ProfileDB(
        user_id=user.id,
        headline=parsed["headline"],
        target_role=target_role,
        readiness_score=readiness,
    )
    db.add(profile_db)
    db.commit()
    db.refresh(profile_db)

    skill_rows = [
        SkillDB(profile_id=profile_db.id, name=name, level=level)
        for name, level in parsed["skills"]
    ]
    exp_rows = [
        ExperienceDB(
            profile_id=profile_db.id,
            title=exp["title"],
            company=exp["company"],
            years=exp["years"],
        )
        for exp in parsed["experiences"]
    ]
    db.add_all(skill_rows + exp_rows)
    db.commit()

    return {
        "filename": file.filename,
        "saved_path": saved_path,
        "profile_id": profile_db.id,
        "readiness_score": readiness,
    }
