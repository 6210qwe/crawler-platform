from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    numbers_data = Column(Text, nullable=False)  # JSON格式存储1000个数字
    total_sum = Column(Integer, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    attempts = Column(Integer, nullable=False, default=0)
    best_time = Column(Integer, nullable=True)  # 最佳完成时间（秒）
    score = Column(Integer, nullable=True)  # 获得的积分
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="challenges")
    exercise = relationship("Exercise", back_populates="challenges")

class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    answer = Column(Integer, nullable=False)
    time_spent = Column(Integer, nullable=False)  # 用时（秒）
    is_correct = Column(Boolean, nullable=False)
    score = Column(Integer, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    challenge = relationship("Challenge")
    user = relationship("User")
