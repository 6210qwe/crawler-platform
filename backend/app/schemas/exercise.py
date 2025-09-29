from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.exercise import DifficultyLevel, ExerciseStatus, SubmissionStatus

class ExerciseBase(BaseModel):
    title: str
    description: str
    target_url: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    points: int = 10
    time_limit: int = 300
    hints: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_url: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    status: Optional[ExerciseStatus] = None
    points: Optional[int] = None
    time_limit: Optional[int] = None
    hints: Optional[str] = None
    solution: Optional[str] = None

class ExerciseInDBBase(ExerciseBase):
    id: int
    status: ExerciseStatus
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Exercise(ExerciseInDBBase):
    pass

class ExerciseSubmissionBase(BaseModel):
    answer: str

class ExerciseSubmissionCreate(ExerciseSubmissionBase):
    pass

class ExerciseSubmissionInDBBase(ExerciseSubmissionBase):
    id: int
    user_id: int
    exercise_id: int
    status: SubmissionStatus
    score: int
    submitted_at: datetime

    class Config:
        from_attributes = True

class ExerciseSubmission(ExerciseSubmissionInDBBase):
    pass

