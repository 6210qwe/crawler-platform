from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User
from app.schemas.knowledge_base import (
    QuestionBank, QuestionBankCreate, QuestionBankUpdate,
    Question, QuestionCreate, QuestionUpdate,
    UserAnswer, UserAnswerCreate,
    WrongQuestion, WrongQuestionDetail,
    ExamSession, ExamSessionCreate,
    StudyStats, StudyStatsSummary,
    ExamSetupRequest, PracticeSetupRequest, ExamResult
)
from app.services.knowledge_base_service import (
    QuestionBankService, QuestionService, ExamService,
    WrongQuestionService, StudyStatsService
)

router = APIRouter()


# 题库管理
@router.get("/banks", response_model=List[QuestionBank])
async def get_question_banks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题库列表"""
    service = QuestionBankService(db)
    return service.get_banks(skip=skip, limit=limit)


@router.post("/banks", response_model=QuestionBank)
async def create_question_bank(
    bank_data: QuestionBankCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建题库"""
    service = QuestionBankService(db)
    return service.create_bank(bank_data)


@router.get("/banks/{bank_id}", response_model=QuestionBank)
async def get_question_bank(
    bank_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题库详情"""
    service = QuestionBankService(db)
    bank = service.get_bank(bank_id)
    if not bank:
        raise HTTPException(status_code=404, detail="题库不存在")
    return bank


@router.put("/banks/{bank_id}", response_model=QuestionBank)
async def update_question_bank(
    bank_id: int,
    bank_data: QuestionBankUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新题库"""
    service = QuestionBankService(db)
    bank = service.update_bank(bank_id, bank_data)
    if not bank:
        raise HTTPException(status_code=404, detail="题库不存在")
    return bank


@router.delete("/banks/{bank_id}")
async def delete_question_bank(
    bank_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除题库"""
    service = QuestionBankService(db)
    success = service.delete_bank(bank_id)
    if not success:
        raise HTTPException(status_code=404, detail="题库不存在")
    return {"message": "题库删除成功"}


# 题目管理
@router.get("/banks/{bank_id}/questions", response_model=List[Question])
async def get_questions(
    bank_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题目列表"""
    service = QuestionService(db)
    return service.get_questions_by_bank(bank_id, skip=skip, limit=limit)


@router.post("/banks/{bank_id}/questions", response_model=Question)
async def create_question(
    bank_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建题目"""
    question_data.bank_id = bank_id
    service = QuestionService(db)
    return service.create_question(question_data)


@router.get("/questions/{question_id}", response_model=Question)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题目详情"""
    service = QuestionService(db)
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question


@router.put("/questions/{question_id}", response_model=Question)
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新题目"""
    service = QuestionService(db)
    question = service.update_question(question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question


@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除题目"""
    service = QuestionService(db)
    success = service.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="题目不存在")
    return {"message": "题目删除成功"}


# 考试功能
@router.post("/exam/setup", response_model=ExamSession)
async def setup_exam(
    setup_data: ExamSetupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """设置考试"""
    service = ExamService(db)
    
    # 生成题目
    questions = service.generate_exam_questions(setup_data.bank_id, setup_data)
    if not questions:
        raise HTTPException(status_code=400, detail="题库中没有足够的题目")
    
    # 创建考试会话
    exam_data = ExamSessionCreate(
        bank_id=setup_data.bank_id,
        exam_type="exam",
        total_questions=len(questions),
        time_limit=setup_data.time_limit * 60 if setup_data.time_limit else None
    )
    
    session = service.create_exam_session(current_user.id, exam_data)
    
    # 返回题目和会话信息
    return session


@router.post("/practice/setup", response_model=ExamSession)
async def setup_practice(
    setup_data: PracticeSetupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """设置刷题"""
    service = ExamService(db)
    
    # 生成题目
    questions = service.generate_practice_questions(setup_data.bank_id, setup_data)
    if not questions:
        raise HTTPException(status_code=400, detail="题库中没有题目")
    
    # 创建刷题会话
    exam_data = ExamSessionCreate(
        bank_id=setup_data.bank_id,
        exam_type="practice",
        total_questions=len(questions)
    )
    
    session = service.create_exam_session(current_user.id, exam_data)
    return session


@router.get("/sessions/{session_id}/questions", response_model=List[Question])
async def get_session_questions(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取会话题目"""
    service = ExamService(db)
    session = service.get_exam_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")
    
    # 根据会话类型生成题目
    if session.exam_type == "exam":
        setup = ExamSetupRequest(
            bank_id=session.bank_id,
            total_questions=session.total_questions,
            single_ratio=40,
            multi_ratio=30,
            bool_ratio=30
        )
        questions = service.generate_exam_questions(session.bank_id, setup)
    else:
        setup = PracticeSetupRequest(
            bank_id=session.bank_id,
            order="顺序"
        )
        questions = service.generate_practice_questions(session.bank_id, setup)
    
    return questions


@router.post("/sessions/{session_id}/submit", response_model=UserAnswer)
async def submit_answer(
    session_id: str,
    answer_data: UserAnswerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交答案"""
    service = ExamService(db)
    session = service.get_exam_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")
    
    if session.is_completed:
        raise HTTPException(status_code=400, detail="考试已完成")
    
    return service.submit_answer(
        current_user.id,
        answer_data.question_id,
        answer_data.answer,
        answer_data.time_spent,
        session_id
    )


@router.post("/sessions/{session_id}/complete", response_model=ExamResult)
async def complete_exam(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """完成考试"""
    service = ExamService(db)
    session = service.get_exam_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")
    
    if session.is_completed:
        raise HTTPException(status_code=400, detail="考试已完成")
    
    completed_session = service.complete_exam(session_id)
    
    # 计算正确率
    accuracy = (completed_session.correct_questions / completed_session.total_questions * 100) if completed_session.total_questions > 0 else 0
    
    return ExamResult(
        session_id=completed_session.session_id,
        total_questions=completed_session.total_questions,
        correct_questions=completed_session.correct_questions,
        total_score=completed_session.total_score,
        user_score=completed_session.user_score,
        accuracy=round(accuracy, 2),
        time_spent=completed_session.time_spent,
        is_completed=completed_session.is_completed
    )


# 错题集
@router.get("/wrong-questions", response_model=List[WrongQuestionDetail])
async def get_wrong_questions(
    bank_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取错题集"""
    service = WrongQuestionService(db)
    wrong_questions = service.get_wrong_questions(current_user.id, bank_id)
    return wrong_questions


@router.post("/wrong-questions/{wrong_question_id}/master")
async def master_question(
    wrong_question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记题目为已掌握"""
    service = WrongQuestionService(db)
    success = service.master_question(wrong_question_id)
    if not success:
        raise HTTPException(status_code=404, detail="错题不存在")
    return {"message": "题目已标记为掌握"}


@router.delete("/wrong-questions/{wrong_question_id}")
async def delete_wrong_question(
    wrong_question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除错题"""
    service = WrongQuestionService(db)
    success = service.delete_wrong_question(wrong_question_id)
    if not success:
        raise HTTPException(status_code=404, detail="错题不存在")
    return {"message": "错题删除成功"}


# 学习统计
@router.get("/stats", response_model=StudyStatsSummary)
async def get_study_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习统计"""
    service = StudyStatsService(db)
    stats = service.get_user_stats(current_user.id)
    return StudyStatsSummary(**stats)


@router.get("/stats/{bank_id}", response_model=StudyStats)
async def get_bank_stats(
    bank_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定题库的学习统计"""
    service = StudyStatsService(db)
    stats = service.get_bank_stats(current_user.id, bank_id)
    if not stats:
        raise HTTPException(status_code=404, detail="统计信息不存在")
    return stats

