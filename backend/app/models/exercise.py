from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)  # 初级、中级、高级、困难、地狱
    challenge_points = Column(Text, nullable=False)  # 挑战要点
    tags = Column(Text, nullable=True)  # JSON格式存储标签数组
    points = Column(Integer, nullable=False, default=10)  # 积分
    is_active = Column(Boolean, nullable=False, default=True)  # 是否启用
    sort_order = Column(Integer, nullable=False, default=0)  # 排序
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 统计字段
    view_count = Column(Integer, nullable=False, default=0)  # 访问次数
    attempt_count = Column(Integer, nullable=False, default=0)  # 尝试次数
    success_count = Column(Integer, nullable=False, default=0)  # 成功次数
    avg_time = Column(Integer, nullable=True)  # 平均完成时间（秒）
    
    # 关系
    submissions = relationship("ExerciseSubmission", back_populates="exercise")
    challenges = relationship("Challenge", back_populates="exercise")

class ExerciseSubmission(Base):
    __tablename__ = "exercise_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    answer = Column(Text, nullable=True)  # 用户答案
    is_correct = Column(Boolean, nullable=False, default=False)
    score = Column(Integer, nullable=True)  # 获得积分
    time_spent = Column(Integer, nullable=True)  # 用时（秒）
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    exercise = relationship("Exercise", back_populates="submissions")
    user = relationship("User", back_populates="exercise_submissions")