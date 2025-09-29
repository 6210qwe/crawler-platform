from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.exercise import Exercise, ExerciseSubmission
from app.schemas.exercise import (
    Exercise as ExerciseSchema, 
    ExerciseCreate, 
    ExerciseUpdate,
    ExerciseSubmission as ExerciseSubmissionSchema,
    ExerciseSubmissionCreate
)
from app.services.exercise_service import ExerciseService
from app.api.api_v1.endpoints.auth import get_current_user as get_current_user_dep

router = APIRouter()

@router.get("/", response_model=List[ExerciseSchema])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    difficulty: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """获取练习题列表"""
    exercise_service = ExerciseService(db)
    exercises = exercise_service.get_exercises(
        skip=skip, 
        limit=limit, 
        difficulty=difficulty
    )
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseSchema)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """获取指定练习题"""
    exercise_service = ExerciseService(db)
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="练习题不存在"
        )
    return exercise

@router.post("/", response_model=ExerciseSchema)
def create_exercise(
    exercise_data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """创建新练习题"""
    exercise_service = ExerciseService(db)
    exercise = exercise_service.create_exercise(exercise_data, current_user.id)
    return exercise

@router.put("/{exercise_id}", response_model=ExerciseSchema)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """更新练习题"""
    exercise_service = ExerciseService(db)
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="练习题不存在"
        )
    
    # 只有创建者或管理员可以更新
    if exercise.created_by != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="没有权限修改此练习题"
        )
    
    updated_exercise = exercise_service.update_exercise(exercise_id, exercise_data)
    return updated_exercise

@router.post("/{exercise_id}/submit", response_model=ExerciseSubmissionSchema)
def submit_exercise(
    exercise_id: int,
    submission_data: ExerciseSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """提交练习题答案"""
    exercise_service = ExerciseService(db)
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="练习题不存在"
        )
    
    submission = exercise_service.submit_exercise(
        exercise_id, 
        current_user.id, 
        submission_data.answer
    )
    return submission

@router.get("/{exercise_id}/submissions", response_model=List[ExerciseSubmissionSchema])
def get_exercise_submissions(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """获取练习题的提交记录"""
    exercise_service = ExerciseService(db)
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="练习题不存在"
        )
    
    # 只有创建者或管理员可以查看所有提交记录
    if exercise.created_by != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="没有权限查看此练习题的提交记录"
        )
    
    submissions = exercise_service.get_exercise_submissions(exercise_id)
    return submissions

