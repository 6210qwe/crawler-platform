from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import json

class ExerciseBase(BaseModel):
    title: str
    description: str
    difficulty: str
    challenge_points: str
    tags: List[str] = []
    points: int = 10
    is_active: bool = True
    sort_order: int = 0

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    challenge_points: Optional[str] = None
    tags: Optional[List[str]] = None
    points: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class ExerciseInDBBase(ExerciseBase):
    id: int
    view_count: int
    attempt_count: int
    success_count: int
    avg_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v or []

    class Config:
        from_attributes = True

class Exercise(ExerciseInDBBase):
    pass

class ExerciseWithStats(Exercise):
    success_rate: float  # 成功率
    difficulty_level: int  # 难度等级（1-5）

class ExerciseSubmissionBase(BaseModel):
    answer: Optional[str] = None
    time_spent: Optional[int] = None

class ExerciseSubmissionCreate(ExerciseSubmissionBase):
    exercise_id: int

class ExerciseSubmission(ExerciseSubmissionBase):
    id: int
    exercise_id: int
    user_id: int
    is_correct: bool
    score: Optional[int] = None
    submitted_at: datetime

    class Config:
        from_attributes = True