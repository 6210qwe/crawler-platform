from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
import uuid
import random
from datetime import datetime

from app.models.knowledge_base import (
    QuestionBank, Question, UserAnswer, WrongQuestion, 
    ExamSession, StudyStats
)
from app.schemas.knowledge_base import (
    QuestionBankCreate, QuestionBankUpdate, QuestionCreate, QuestionUpdate,
    UserAnswerCreate, WrongQuestionCreate, ExamSessionCreate,
    ExamSetupRequest, PracticeSetupRequest
)


class QuestionBankService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_bank(self, bank_data: QuestionBankCreate) -> QuestionBank:
        """创建题库"""
        db_bank = QuestionBank(**bank_data.dict())
        self.db.add(db_bank)
        self.db.commit()
        self.db.refresh(db_bank)
        return db_bank
    
    def get_bank(self, bank_id: int) -> Optional[QuestionBank]:
        """获取题库"""
        return self.db.query(QuestionBank).filter(
            QuestionBank.id == bank_id,
            QuestionBank.is_active == True
        ).first()
    
    def get_banks(self, skip: int = 0, limit: int = 100) -> List[QuestionBank]:
        """获取题库列表"""
        banks = self.db.query(QuestionBank).filter(
            QuestionBank.is_active == True
        ).offset(skip).limit(limit).all()
        
        # 添加题目数量
        for bank in banks:
            bank.question_count = self.db.query(Question).filter(
                Question.bank_id == bank.id,
                Question.is_active == True
            ).count()
        
        return banks
    
    def update_bank(self, bank_id: int, bank_data: QuestionBankUpdate) -> Optional[QuestionBank]:
        """更新题库"""
        db_bank = self.get_bank(bank_id)
        if not db_bank:
            return None
        
        update_data = bank_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bank, field, value)
        
        self.db.commit()
        self.db.refresh(db_bank)
        return db_bank
    
    def delete_bank(self, bank_id: int) -> bool:
        """删除题库（软删除）"""
        db_bank = self.get_bank(bank_id)
        if not db_bank:
            return False
        
        db_bank.is_active = False
        self.db.commit()
        return True


class QuestionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_question(self, question_data: QuestionCreate) -> Question:
        """创建题目"""
        db_question = Question(**question_data.dict())
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """获取题目"""
        return self.db.query(Question).filter(
            Question.id == question_id,
            Question.is_active == True
        ).first()
    
    def get_questions_by_bank(self, bank_id: int, skip: int = 0, limit: int = 100) -> List[Question]:
        """根据题库获取题目列表"""
        return self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_questions_by_type(self, bank_id: int, question_type: str) -> List[Question]:
        """根据题型获取题目"""
        return self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.type == question_type,
            Question.is_active == True
        ).all()
    
    def update_question(self, question_id: int, question_data: QuestionUpdate) -> Optional[Question]:
        """更新题目"""
        db_question = self.get_question(question_id)
        if not db_question:
            return None
        
        update_data = question_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_question, field, value)
        
        self.db.commit()
        self.db.refresh(db_question)
        return db_question
    
    def delete_question(self, question_id: int) -> bool:
        """删除题目（软删除）"""
        db_question = self.get_question(question_id)
        if not db_question:
            return False
        
        db_question.is_active = False
        self.db.commit()
        return True


class ExamService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_exam_session(self, user_id: int, exam_data: ExamSessionCreate) -> ExamSession:
        """创建考试会话"""
        session_id = str(uuid.uuid4())
        db_session = ExamSession(
            user_id=user_id,
            session_id=session_id,
            **exam_data.dict()
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    def get_exam_session(self, session_id: str) -> Optional[ExamSession]:
        """获取考试会话"""
        return self.db.query(ExamSession).filter(
            ExamSession.session_id == session_id
        ).first()
    
    def generate_exam_questions(self, bank_id: int, setup: ExamSetupRequest) -> List[Question]:
        """生成考试题目"""
        # 按题型获取题目
        single_questions = self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.type == "单选题",
            Question.is_active == True
        ).all()
        
        multi_questions = self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.type == "多选题",
            Question.is_active == True
        ).all()
        
        bool_questions = self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.type == "判断题",
            Question.is_active == True
        ).all()
        
        # 计算各题型题目数量
        single_count = int(setup.total_questions * setup.single_ratio / 100)
        multi_count = int(setup.total_questions * setup.multi_ratio / 100)
        bool_count = setup.total_questions - single_count - multi_count
        
        # 随机选择题目
        selected_questions = []
        
        if single_count > 0 and single_questions:
            selected_questions.extend(random.sample(single_questions, min(single_count, len(single_questions))))
        
        if multi_count > 0 and multi_questions:
            selected_questions.extend(random.sample(multi_questions, min(multi_count, len(multi_questions))))
        
        if bool_count > 0 and bool_questions:
            selected_questions.extend(random.sample(bool_questions, min(bool_count, len(bool_questions))))
        
        # 如果题目不足，补充随机题目
        if len(selected_questions) < setup.total_questions:
            remaining = setup.total_questions - len(selected_questions)
            all_questions = self.db.query(Question).filter(
                Question.bank_id == bank_id,
                Question.is_active == True
            ).all()
            
            remaining_questions = [q for q in all_questions if q not in selected_questions]
            if remaining_questions:
                selected_questions.extend(random.sample(remaining_questions, min(remaining, len(remaining_questions))))
        
        # 随机排序
        random.shuffle(selected_questions)
        return selected_questions
    
    def generate_practice_questions(self, bank_id: int, setup: PracticeSetupRequest) -> List[Question]:
        """生成刷题题目"""
        questions = self.db.query(Question).filter(
            Question.bank_id == bank_id,
            Question.is_active == True
        ).all()
        
        if setup.order == "逆序":
            questions.reverse()
        elif setup.order == "随机":
            random.shuffle(questions)
        
        return questions
    
    def submit_answer(self, user_id: int, question_id: int, answer: str, 
                     time_spent: int, session_id: str) -> UserAnswer:
        """提交答案"""
        # 获取题目
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("题目不存在")
        
        # 判断答案是否正确
        is_correct = self._check_answer(question, answer)
        score = question.score if is_correct else 0
        
        # 创建答题记录
        db_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            answer=answer,
            is_correct=is_correct,
            score=score,
            time_spent=time_spent,
            session_id=session_id
        )
        self.db.add(db_answer)
        
        # 更新考试会话
        exam_session = self.db.query(ExamSession).filter(
            ExamSession.session_id == session_id
        ).first()
        if exam_session:
            exam_session.answered_questions += 1
            if is_correct:
                exam_session.correct_questions += 1
            exam_session.user_score += score
            exam_session.time_spent += time_spent
        
        # 如果答错了，添加到错题集
        if not is_correct:
            self._add_to_wrong_questions(user_id, question_id, answer)
        
        # 更新学习统计
        self._update_study_stats(user_id, question.bank_id, is_correct, score, time_spent)
        
        self.db.commit()
        self.db.refresh(db_answer)
        return db_answer
    
    def complete_exam(self, session_id: str) -> ExamSession:
        """完成考试"""
        exam_session = self.db.query(ExamSession).filter(
            ExamSession.session_id == session_id
        ).first()
        if not exam_session:
            raise ValueError("考试会话不存在")
        
        exam_session.is_completed = True
        exam_session.completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(exam_session)
        return exam_session
    
    def _check_answer(self, question: Question, user_answer: str) -> bool:
        """检查答案是否正确"""
        correct_answer = question.answer
        
        if question.type == "多选题":
            # 对多选题答案进行排序比较
            user_answer_sorted = "".join(sorted(user_answer.upper()))
            correct_answer_sorted = "".join(sorted(correct_answer.replace(", ", "").upper()))
            return user_answer_sorted == correct_answer_sorted
        elif question.type in ["填空题", "问答题"]:
            return str(user_answer).strip().upper() == str(correct_answer).strip().upper()
        else:
            return str(user_answer).upper() == str(correct_answer).upper()
    
    def _add_to_wrong_questions(self, user_id: int, question_id: int, user_answer: str):
        """添加到错题集"""
        # 检查是否已存在
        existing = self.db.query(WrongQuestion).filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.question_id == question_id,
            WrongQuestion.is_mastered == False
        ).first()
        
        if existing:
            existing.wrong_count += 1
            existing.user_answer = user_answer
            existing.last_wrong_at = datetime.utcnow()
        else:
            wrong_question = WrongQuestion(
                user_id=user_id,
                question_id=question_id,
                user_answer=user_answer
            )
            self.db.add(wrong_question)
    
    def _update_study_stats(self, user_id: int, bank_id: int, is_correct: bool, score: int, time_spent: int):
        """更新学习统计"""
        stats = self.db.query(StudyStats).filter(
            StudyStats.user_id == user_id,
            StudyStats.bank_id == bank_id
        ).first()
        
        if not stats:
            stats = StudyStats(
                user_id=user_id,
                bank_id=bank_id
            )
            self.db.add(stats)
        
        stats.answered_questions += 1
        if is_correct:
            stats.correct_questions += 1
        stats.total_score += score
        stats.study_time += time_spent
        stats.last_study_at = datetime.utcnow()


class WrongQuestionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_wrong_questions(self, user_id: int, bank_id: Optional[int] = None) -> List[WrongQuestion]:
        """获取错题集"""
        query = self.db.query(WrongQuestion).filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.is_mastered == False
        )
        
        if bank_id:
            query = query.join(Question).filter(Question.bank_id == bank_id)
        
        return query.all()
    
    def master_question(self, wrong_question_id: int) -> bool:
        """标记题目为已掌握"""
        wrong_question = self.db.query(WrongQuestion).filter(
            WrongQuestion.id == wrong_question_id
        ).first()
        
        if not wrong_question:
            return False
        
        wrong_question.is_mastered = True
        wrong_question.mastered_at = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def delete_wrong_question(self, wrong_question_id: int) -> bool:
        """删除错题"""
        wrong_question = self.db.query(WrongQuestion).filter(
            WrongQuestion.id == wrong_question_id
        ).first()
        
        if not wrong_question:
            return False
        
        self.db.delete(wrong_question)
        self.db.commit()
        return True


class StudyStatsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """获取用户学习统计"""
        # 获取总体统计
        total_stats = self.db.query(
            func.count(StudyStats.id).label('total_banks'),
            func.sum(StudyStats.total_questions).label('total_questions'),
            func.sum(StudyStats.answered_questions).label('answered_questions'),
            func.sum(StudyStats.correct_questions).label('correct_questions'),
            func.sum(StudyStats.total_score).label('total_score'),
            func.sum(StudyStats.study_time).label('study_time')
        ).filter(StudyStats.user_id == user_id).first()
        
        # 获取错题统计
        wrong_count = self.db.query(WrongQuestion).filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.is_mastered == False
        ).count()
        
        mastered_count = self.db.query(WrongQuestion).filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.is_mastered == True
        ).count()
        
        # 计算正确率
        answered = total_stats.answered_questions or 0
        correct = total_stats.correct_questions or 0
        accuracy = (correct / answered * 100) if answered > 0 else 0
        
        return {
            "total_banks": total_stats.total_banks or 0,
            "total_questions": total_stats.total_questions or 0,
            "answered_questions": answered,
            "correct_questions": correct,
            "total_score": total_stats.total_score or 0,
            "study_time": total_stats.study_time or 0,
            "accuracy": round(accuracy, 2),
            "wrong_questions_count": wrong_count,
            "mastered_questions_count": mastered_count
        }
    
    def get_bank_stats(self, user_id: int, bank_id: int) -> Optional[StudyStats]:
        """获取特定题库的学习统计"""
        return self.db.query(StudyStats).filter(
            StudyStats.user_id == user_id,
            StudyStats.bank_id == bank_id
        ).first()

