from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChallengeBase(BaseModel):
    exercise_id: int

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeMetaResponse(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    total_sum: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    attempts: int
    best_time: Optional[int] = None
    score: Optional[int] = None
    total_pages: int

    class Config:
        from_attributes = True

class ChallengePageResponse(BaseModel):
    page_number: int
    numbers: List[int]
    start_index: int
    end_index: int

class ChallengeSubmission(BaseModel):
    exercise_id: int
    answer: int
    time_spent: int

class ChallengeSubmissionResponse(BaseModel):
    id: int
    challenge_id: int
    user_id: int
    exercise_id: int
    answer: int
    time_spent: int
    is_correct: bool
    score: Optional[int] = None
    submitted_at: datetime

    class Config:
        from_attributes = True

class UserProgress(BaseModel):
    completed_challenges: List[int]
    total_score: int
    total_attempts: int
    average_time: int

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: int
    completed_at: Optional[str] = None
    time_spent: int
