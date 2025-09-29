from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DifficultyLevel(enum.Enum):
    BEGINNER = "beginner"   # 初级
    INTERMEDIATE = "intermediate"  # 中级
    ADVANCED = "advanced"   # 高级
    HARD = "hard"           # 困难
    HELL = "hell"           # 地狱

class ExerciseStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class SubmissionStatus(enum.Enum):
    PENDING = "pending"
    CORRECT = "correct"
    INCORRECT = "incorrect"
    TIMEOUT = "timeout"

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    target_url = Column(String(500), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    status = Column(Enum(ExerciseStatus), default=ExerciseStatus.DRAFT)
    points = Column(Integer, default=10)
    time_limit = Column(Integer, default=300)  # 秒
    hints = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    creator = relationship("User", back_populates="created_exercises")
    submissions = relationship("ExerciseSubmission", back_populates="exercise")

class ExerciseSubmission(Base):
    __tablename__ = "exercise_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    answer = Column(Text, nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    score = Column(Integer, default=0)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")

