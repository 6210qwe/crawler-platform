from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user_optional
from app.models.user import User
from app.services.exercise_service import ExerciseService
from app.schemas.exercise import Exercise, ExerciseCreate, ExerciseUpdate, ExerciseSubmission, ExerciseSubmissionCreate

router = APIRouter()

@router.get("/", response_model=List[Exercise])
async def list_exercises(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("sort_order"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """获取题目列表"""
    service = ExerciseService(db)
    exercises = service.get_all(skip=skip, limit=limit, difficulty=difficulty, 
                              search=search, sort_by=sort_by)
    return exercises

@router.get("/count")
async def count_exercises(
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取符合筛选条件的题目总数（用于分页）"""
    service = ExerciseService(db)
    total = service.get_count(difficulty=difficulty, search=search)
    return {"total": total}

@router.get("/{exercise_id}", response_model=Exercise)
async def get_exercise_by_id(
    exercise_id: int,
    db: Session = Depends(get_db)
):
    """获取单个题目详情"""
    service = ExerciseService(db)
    exercise = service.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="题目不存在")
    return exercise

@router.get("/statistics/overview")
async def get_exercise_statistics(db: Session = Depends(get_db)):
    """获取题目统计信息"""
    service = ExerciseService(db)
    stats = service.get_statistics()
    return stats

@router.post("/{exercise_id}/submit", response_model=ExerciseSubmission)
async def submit_exercise_answer(
    exercise_id: int,
    submission_data: ExerciseSubmissionCreate,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """提交题目答案"""
    if not current_user:
        raise HTTPException(status_code=401, detail="需要登录")
    
    service = ExerciseService(db)
    try:
        submission = service.submit_answer(
            exercise_id=exercise_id,
            user_id=current_user.id,
            answer=submission_data.answer,
            time_spent=submission_data.time_spent
        )
        return submission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/progress")
async def get_user_progress(
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """获取用户进度"""
    if not current_user:
        raise HTTPException(status_code=401, detail="需要登录")
    
    service = ExerciseService(db)
    progress = service.get_user_progress(current_user.id)
    return progress
