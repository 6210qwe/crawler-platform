from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.exercise import Exercise, ExerciseSubmission, DifficultyLevel, SubmissionStatus
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate
from typing import List, Optional

class ExerciseService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_exercises(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        difficulty: Optional[str] = None
    ) -> List[Exercise]:
        query = self.db.query(Exercise).filter(Exercise.status == "published")
        
        if difficulty:
            # 兼容字符串传参
            try:
                level = DifficultyLevel(difficulty)
                query = query.filter(Exercise.difficulty == level)
            except ValueError:
                pass
        
        return query.offset(skip).limit(limit).all()
    
    def get_exercise_by_id(self, exercise_id: int) -> Exercise:
        return self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    def create_exercise(self, exercise_data: ExerciseCreate, created_by: int) -> Exercise:
        db_exercise = Exercise(
            title=exercise_data.title,
            description=exercise_data.description,
            target_url=exercise_data.target_url,
            difficulty=exercise_data.difficulty,
            points=exercise_data.points,
            time_limit=exercise_data.time_limit,
            hints=exercise_data.hints,
            created_by=created_by
        )
        self.db.add(db_exercise)
        self.db.commit()
        self.db.refresh(db_exercise)
        return db_exercise
    
    def update_exercise(self, exercise_id: int, exercise_data: ExerciseUpdate) -> Exercise:
        db_exercise = self.get_exercise_by_id(exercise_id)
        if not db_exercise:
            return None
        
        update_data = exercise_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_exercise, field, value)
        
        self.db.commit()
        self.db.refresh(db_exercise)
        return db_exercise
    
    def submit_exercise(
        self, 
        exercise_id: int, 
        user_id: int, 
        answer: str
    ) -> ExerciseSubmission:
        # 检查是否已经提交过
        existing_submission = self.db.query(ExerciseSubmission).filter(
            and_(
                ExerciseSubmission.exercise_id == exercise_id,
                ExerciseSubmission.user_id == user_id
            )
        ).first()
        
        if existing_submission:
            # 更新现有提交
            existing_submission.answer = answer
            existing_submission.status = SubmissionStatus.PENDING
            self.db.commit()
            self.db.refresh(existing_submission)
            return existing_submission
        else:
            # 创建新提交
            db_submission = ExerciseSubmission(
                user_id=user_id,
                exercise_id=exercise_id,
                answer=answer,
                status=SubmissionStatus.PENDING
            )
            self.db.add(db_submission)
            self.db.commit()
            self.db.refresh(db_submission)
            return db_submission
    
    def get_exercise_submissions(self, exercise_id: int) -> List[ExerciseSubmission]:
        return self.db.query(ExerciseSubmission).filter(
            ExerciseSubmission.exercise_id == exercise_id
        ).all()
    
    def get_user_submissions(self, user_id: int) -> List[ExerciseSubmission]:
        return self.db.query(ExerciseSubmission).filter(
            ExerciseSubmission.user_id == user_id
        ).all()

