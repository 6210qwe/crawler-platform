from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
import json
from app.models.exercise import Exercise, ExerciseSubmission
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate

class ExerciseService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, difficulty: Optional[str] = None, 
                search: Optional[str] = None, sort_by: str = "sort_order") -> List[Exercise]:
        """获取所有题目"""
        query = self.db.query(Exercise).filter(Exercise.is_active == True)
        
        # 难度筛选
        if difficulty:
            query = query.filter(Exercise.difficulty == difficulty)
        
        # 搜索
        if search:
            query = query.filter(
                Exercise.title.contains(search) | 
                Exercise.description.contains(search)
            )
        
        # 排序
        if sort_by == "difficulty":
            difficulty_order = {"初级": 1, "中级": 2, "高级": 3, "困难": 4, "地狱": 5}
            query = query.order_by(Exercise.difficulty)
        elif sort_by == "points":
            query = query.order_by(desc(Exercise.points))
        elif sort_by == "popular":
            query = query.order_by(desc(Exercise.view_count))
        else:
            query = query.order_by(asc(Exercise.sort_order), asc(Exercise.id))
        
        return query.offset(skip).limit(limit).all()

    def get_count(self, difficulty: Optional[str] = None, search: Optional[str] = None) -> int:
        """获取符合筛选条件的题目总数"""
        query = self.db.query(Exercise).filter(Exercise.is_active == True)

        if difficulty:
            query = query.filter(Exercise.difficulty == difficulty)

        if search:
            query = query.filter(
                Exercise.title.contains(search) |
                Exercise.description.contains(search)
            )

        return query.count()

    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """根据ID获取题目"""
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if exercise:
            # 增加访问次数
            exercise.view_count += 1
            self.db.commit()
        return exercise

    def create(self, exercise_data: ExerciseCreate) -> Exercise:
        """创建新题目"""
        exercise = Exercise(
            title=exercise_data.title,
            description=exercise_data.description,
            difficulty=exercise_data.difficulty,
            challenge_points=exercise_data.challenge_points,
            tags=json.dumps(exercise_data.tags, ensure_ascii=False),
            points=exercise_data.points,
            is_active=exercise_data.is_active,
            sort_order=exercise_data.sort_order
        )
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def update(self, exercise_id: int, exercise_data: ExerciseUpdate) -> Optional[Exercise]:
        """更新题目"""
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return None
        
        update_data = exercise_data.dict(exclude_unset=True)
        if "tags" in update_data:
            update_data["tags"] = json.dumps(update_data["tags"], ensure_ascii=False)
        
        for field, value in update_data.items():
            setattr(exercise, field, value)
        
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def delete(self, exercise_id: int) -> bool:
        """删除题目（软删除）"""
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return False
        
        exercise.is_active = False
        self.db.commit()
        return True

    def get_statistics(self) -> dict:
        """获取题目统计信息"""
        total = self.db.query(Exercise).filter(Exercise.is_active == True).count()
        by_difficulty = {}
        
        for difficulty in ["初级", "中级", "高级", "困难", "地狱"]:
            count = self.db.query(Exercise).filter(
                Exercise.is_active == True,
                Exercise.difficulty == difficulty
            ).count()
            by_difficulty[difficulty] = count
        
        return {
            "total": total,
            "by_difficulty": by_difficulty
        }

    def submit_answer(self, exercise_id: int, user_id: int, answer: str, 
                     time_spent: Optional[int] = None) -> ExerciseSubmission:
        """提交答案"""
        exercise = self.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("题目不存在")
        
        # 这里可以添加答案验证逻辑
        is_correct = self._validate_answer(exercise, answer)
        score = exercise.points if is_correct else 0
        
        # 更新题目统计
        exercise.attempt_count += 1
        if is_correct:
            exercise.success_count += 1
            if time_spent:
                # 更新平均时间
                if exercise.avg_time:
                    exercise.avg_time = (exercise.avg_time + time_spent) // 2
                else:
                    exercise.avg_time = time_spent
        
        submission = ExerciseSubmission(
            exercise_id=exercise_id,
            user_id=user_id,
            answer=answer,
            is_correct=is_correct,
            score=score,
            time_spent=time_spent
        )
        
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def _validate_answer(self, exercise: Exercise, answer: str) -> bool:
        """验证答案（这里需要根据具体题目类型实现）"""
        # 对于数字求和题目，这里应该调用challenge服务验证
        # 暂时返回True作为示例
        return True

    def get_user_progress(self, user_id: int) -> dict:
        """获取用户进度"""
        submissions = self.db.query(ExerciseSubmission).filter(
            ExerciseSubmission.user_id == user_id
        ).all()
        
        completed = len([s for s in submissions if s.is_correct])
        total_score = sum(s.score or 0 for s in submissions)
        
        return {
            "total_attempts": len(submissions),
            "completed_exercises": completed,
            "total_score": total_score
        }