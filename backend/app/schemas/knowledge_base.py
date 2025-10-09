from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class QuestionBankBase(BaseModel):
    name: str = Field(..., description="题库名称")
    description: Optional[str] = Field(None, description="题库描述")


class QuestionBankCreate(QuestionBankBase):
    pass


class QuestionBankUpdate(BaseModel):
    name: Optional[str] = Field(None, description="题库名称")
    description: Optional[str] = Field(None, description="题库描述")
    is_active: Optional[bool] = Field(None, description="是否激活")


class QuestionBank(QuestionBankBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    question_count: Optional[int] = Field(None, description="题目数量")
    
    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    type: str = Field(..., description="题型")
    question: str = Field(..., description="题目内容")
    options: Optional[List[str]] = Field(None, description="选项")
    answer: str = Field(..., description="正确答案")
    explanation: Optional[str] = Field(None, description="解析")
    score: int = Field(1, description="分值")
    difficulty: str = Field("简单", description="难度")


class QuestionCreate(QuestionBase):
    bank_id: int = Field(..., description="题库ID")


class QuestionUpdate(BaseModel):
    type: Optional[str] = Field(None, description="题型")
    question: Optional[str] = Field(None, description="题目内容")
    options: Optional[List[str]] = Field(None, description="选项")
    answer: Optional[str] = Field(None, description="正确答案")
    explanation: Optional[str] = Field(None, description="解析")
    score: Optional[int] = Field(None, description="分值")
    difficulty: Optional[str] = Field(None, description="难度")
    is_active: Optional[bool] = Field(None, description="是否激活")


class Question(QuestionBase):
    id: int
    bank_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserAnswerBase(BaseModel):
    question_id: int = Field(..., description="题目ID")
    answer: str = Field(..., description="用户答案")
    time_spent: int = Field(0, description="用时（秒）")


class UserAnswerCreate(UserAnswerBase):
    session_id: Optional[str] = Field(None, description="答题会话ID")


class UserAnswer(UserAnswerBase):
    id: int
    user_id: int
    is_correct: bool
    score: int
    session_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class WrongQuestionBase(BaseModel):
    question_id: int = Field(..., description="题目ID")
    user_answer: str = Field(..., description="用户错误答案")


class WrongQuestionCreate(WrongQuestionBase):
    pass


class WrongQuestion(WrongQuestionBase):
    id: int
    user_id: int
    wrong_count: int
    last_wrong_at: datetime
    is_mastered: bool
    mastered_at: Optional[datetime] = None
    created_at: datetime
    question: Optional[Question] = None
    
    class Config:
        from_attributes = True


class ExamSessionBase(BaseModel):
    bank_id: int = Field(..., description="题库ID")
    exam_type: str = Field(..., description="考试类型")
    total_questions: int = Field(..., description="总题数")
    time_limit: Optional[int] = Field(None, description="时间限制（秒）")


class ExamSessionCreate(ExamSessionBase):
    pass


class ExamSession(ExamSessionBase):
    id: int
    user_id: int
    session_id: str
    answered_questions: int
    correct_questions: int
    total_score: int
    user_score: int
    time_spent: int
    is_completed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class StudyStatsBase(BaseModel):
    bank_id: int = Field(..., description="题库ID")


class StudyStats(StudyStatsBase):
    id: int
    user_id: int
    total_questions: int
    answered_questions: int
    correct_questions: int
    total_score: int
    study_time: int
    last_study_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ExamSetupRequest(BaseModel):
    bank_id: int = Field(..., description="题库ID")
    total_questions: int = Field(..., description="题目数量")
    single_ratio: int = Field(40, description="单选题比例")
    multi_ratio: int = Field(30, description="多选题比例")
    bool_ratio: int = Field(30, description="判断题比例")
    time_limit: Optional[int] = Field(None, description="时间限制（分钟）")


class PracticeSetupRequest(BaseModel):
    bank_id: int = Field(..., description="题库ID")
    order: str = Field("顺序", description="刷题顺序：顺序、逆序、随机")


class ExamResult(BaseModel):
    session_id: str
    total_questions: int
    correct_questions: int
    total_score: int
    user_score: int
    accuracy: float
    time_spent: int
    is_completed: bool


class QuestionWithAnswer(Question):
    user_answer: Optional[str] = Field(None, description="用户答案")
    is_correct: Optional[bool] = Field(None, description="是否正确")


class WrongQuestionDetail(WrongQuestion):
    question: Question = Field(..., description="题目详情")


class StudyStatsSummary(BaseModel):
    total_banks: int = Field(0, description="总题库数")
    total_questions: int = Field(0, description="总题数")
    answered_questions: int = Field(0, description="已答题数")
    correct_questions: int = Field(0, description="正确题数")
    total_score: int = Field(0, description="总得分")
    study_time: int = Field(0, description="学习时间（秒）")
    accuracy: float = Field(0.0, description="正确率")
    wrong_questions_count: int = Field(0, description="错题数")
    mastered_questions_count: int = Field(0, description="已掌握题数")

