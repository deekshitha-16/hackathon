from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)

    profiles = relationship("ProfileDB", back_populates="user")


class ProfileDB(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    headline = Column(String)
    target_role = Column(String)
    readiness_score = Column(Integer)

    user = relationship("User", back_populates="profiles")
    skills = relationship("SkillDB", back_populates="profile")
    experiences = relationship("ExperienceDB", back_populates="profile")


class SkillDB(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    name = Column(String, index=True)
    level = Column(Integer)

    profile = relationship("ProfileDB", back_populates="skills")


class ExperienceDB(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    company = Column(String)
    years = Column(Float)

    profile = relationship("ProfileDB", back_populates="experiences")
