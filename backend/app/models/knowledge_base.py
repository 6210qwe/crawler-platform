from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class QuestionBank(Base):
    """题库表"""
    __tablename__ = "question_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, comment="题库名称")
    description = Column(Text, comment="题库描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 关联关系
    questions = relationship("Question", back_populates="bank", cascade="all, delete-orphan")


class Question(Base):
    """题目表"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(Integer, ForeignKey("question_banks.id"), nullable=False, comment="题库ID")
    type = Column(String(20), nullable=False, comment="题型：单选题、多选题、判断题、填空题、问答题")
    question = Column(Text, nullable=False, comment="题目内容")
    options = Column(JSON, comment="选项（JSON格式）")
    answer = Column(Text, nullable=False, comment="正确答案")
    explanation = Column(Text, comment="解析")
    score = Column(Integer, default=1, comment="分值")
    difficulty = Column(String(20), default="简单", comment="难度：简单、中等、困难")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 关联关系
    bank = relationship("QuestionBank", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan")
    wrong_questions = relationship("WrongQuestion", back_populates="question", cascade="all, delete-orphan")


class UserAnswer(Base):
    """用户答题记录表"""
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="题目ID")
    answer = Column(Text, comment="用户答案")
    is_correct = Column(Boolean, comment="是否正确")
    score = Column(Integer, default=0, comment="得分")
    time_spent = Column(Integer, default=0, comment="用时（秒）")
    session_id = Column(String(100), comment="答题会话ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="答题时间")
    
    # 关联关系
    user = relationship("User")
    question = relationship("Question", back_populates="user_answers")


class WrongQuestion(Base):
    """错题集表"""
    __tablename__ = "wrong_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="题目ID")
    user_answer = Column(Text, comment="用户错误答案")
    wrong_count = Column(Integer, default=1, comment="错误次数")
    last_wrong_at = Column(DateTime(timezone=True), server_default=func.now(), comment="最后错误时间")
    is_mastered = Column(Boolean, default=False, comment="是否已掌握")
    mastered_at = Column(DateTime(timezone=True), comment="掌握时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 关联关系
    user = relationship("User")
    question = relationship("Question", back_populates="wrong_questions")


class ExamSession(Base):
    """考试会话表"""
    __tablename__ = "exam_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    bank_id = Column(Integer, ForeignKey("question_banks.id"), nullable=False, comment="题库ID")
    session_id = Column(String(100), unique=True, nullable=False, comment="会话ID")
    exam_type = Column(String(20), nullable=False, comment="考试类型：exam（考试）、practice（刷题）")
    total_questions = Column(Integer, nullable=False, comment="总题数")
    answered_questions = Column(Integer, default=0, comment="已答题数")
    correct_questions = Column(Integer, default=0, comment="正确题数")
    total_score = Column(Integer, default=0, comment="总分")
    user_score = Column(Integer, default=0, comment="用户得分")
    time_limit = Column(Integer, comment="时间限制（秒）")
    time_spent = Column(Integer, default=0, comment="已用时间（秒）")
    is_completed = Column(Boolean, default=False, comment="是否完成")
    started_at = Column(DateTime(timezone=True), server_default=func.now(), comment="开始时间")
    completed_at = Column(DateTime(timezone=True), comment="完成时间")
    
    # 关联关系
    user = relationship("User")
    bank = relationship("QuestionBank")


class StudyStats(Base):
    """学习统计表"""
    __tablename__ = "study_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    bank_id = Column(Integer, ForeignKey("question_banks.id"), nullable=False, comment="题库ID")
    total_questions = Column(Integer, default=0, comment="总题数")
    answered_questions = Column(Integer, default=0, comment="已答题数")
    correct_questions = Column(Integer, default=0, comment="正确题数")
    total_score = Column(Integer, default=0, comment="总得分")
    study_time = Column(Integer, default=0, comment="学习时间（秒）")
    last_study_at = Column(DateTime(timezone=True), comment="最后学习时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    user = relationship("User")
    bank = relationship("QuestionBank")

