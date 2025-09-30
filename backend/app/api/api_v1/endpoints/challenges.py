from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import random
from datetime import datetime

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, ChallengeSubmission
from app.schemas.challenge import ChallengeCreate, ChallengeResponse, ChallengeSubmission as ChallengeSubmissionSchema, ChallengePageResponse

router = APIRouter()

def generate_challenge_numbers(user_id: int, exercise_id: int) -> tuple[List[List[int]], int]:
    """生成用户特定的挑战数字"""
    numbers = []
    total_sum = 0
    
    for page in range(100):
        page_numbers = []
        for i in range(10):
            # 使用用户ID和题目ID作为种子，确保每个用户的数据不同
            seed = (user_id * 1000 + exercise_id * 100 + page * 10 + i) % 200 + 1
            page_numbers.append(seed)
            total_sum += seed
        numbers.append(page_numbers)
    
    return numbers, total_sum

@router.get("/{exercise_id}", response_model=ChallengeResponse)
async def get_challenge(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取或创建挑战数据"""
    # 查找现有挑战
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == exercise_id
    ).first()
    
    if not challenge:
        # 创建新挑战
        numbers, total_sum = generate_challenge_numbers(current_user.id, exercise_id)
        
        challenge = Challenge(
            user_id=current_user.id,
            exercise_id=exercise_id,
            numbers_data=json.dumps(numbers),
            total_sum=total_sum
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
    else:
        # 解析现有数据
        numbers = json.loads(challenge.numbers_data)
        total_sum = challenge.total_sum
    
    return ChallengeResponse(
        id=challenge.id,
        user_id=challenge.user_id,
        exercise_id=challenge.exercise_id,
        numbers=numbers,
        total_sum=total_sum,
        is_completed=challenge.is_completed,
        completed_at=challenge.completed_at,
        attempts=challenge.attempts,
        best_time=challenge.best_time,
        score=challenge.score
    )

@router.get("/{exercise_id}/page/{page_number}", response_model=ChallengePageResponse)
async def get_challenge_page(
    exercise_id: int,
    page_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取挑战页面数据"""
    if page_number < 1 or page_number > 100:
        raise HTTPException(status_code=400, detail="页面编号必须在1-100之间")
    
    # 查找挑战数据
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == exercise_id
    ).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    numbers = json.loads(challenge.numbers_data)
    page_numbers = numbers[page_number - 1]
    
    return ChallengePageResponse(
        page_number=page_number,
        numbers=page_numbers,
        start_index=(page_number - 1) * 10 + 1,
        end_index=page_number * 10
    )

@router.post("/submit")
async def submit_challenge(
    submission: ChallengeSubmissionSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交挑战答案"""
    # 查找挑战数据
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == submission.exercise_id
    ).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    # 检查答案是否正确
    is_correct = submission.answer == challenge.total_sum
    
    # 记录提交
    submission_record = ChallengeSubmission(
        challenge_id=challenge.id,
        user_id=current_user.id,
        exercise_id=submission.exercise_id,
        answer=submission.answer,
        time_spent=submission.time_spent,
        is_correct=is_correct
    )
    
    # 更新挑战状态
    challenge.attempts += 1
    
    if is_correct and not challenge.is_completed:
        challenge.is_completed = True
        challenge.completed_at = datetime.utcnow()
        challenge.best_time = submission.time_spent
        # 根据难度和用时计算积分
        base_score = 100  # 基础积分
        time_bonus = max(0, 300 - submission.time_spent) // 10  # 时间奖励
        challenge.score = base_score + time_bonus
        submission_record.score = challenge.score
    
    db.add(submission_record)
    db.commit()
    
    return {
        "success": True,
        "message": "恭喜！答案正确！" if is_correct else "答案错误，请重新尝试",
        "is_correct": is_correct,
        "correct_answer": challenge.total_sum if not is_correct else None,
        "score": challenge.score if is_correct else None,
        "completed_at": challenge.completed_at.isoformat() if challenge.is_completed else None
    }

@router.get("/progress")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户挑战进度"""
    # 获取已完成的挑战
    completed_challenges = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.is_completed == True
    ).all()
    
    # 获取总积分
    total_score = sum(challenge.score or 0 for challenge in completed_challenges)
    
    # 获取总尝试次数
    total_attempts = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.user_id == current_user.id
    ).count()
    
    # 获取平均用时
    completed_times = [challenge.best_time for challenge in completed_challenges if challenge.best_time]
    average_time = sum(completed_times) / len(completed_times) if completed_times else 0
    
    return {
        "completed_challenges": [challenge.exercise_id for challenge in completed_challenges],
        "total_score": total_score,
        "total_attempts": total_attempts,
        "average_time": int(average_time)
    }

@router.get("/leaderboard")
async def get_leaderboard(
    exercise_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取挑战排行榜"""
    query = db.query(Challenge).filter(Challenge.is_completed == True)
    
    if exercise_id:
        query = query.filter(Challenge.exercise_id == exercise_id)
    
    challenges = query.order_by(Challenge.score.desc(), Challenge.best_time.asc()).limit(limit).all()
    
    leaderboard = []
    for rank, challenge in enumerate(challenges, 1):
        leaderboard.append({
            "rank": rank,
            "username": challenge.user.username,
            "score": challenge.score or 0,
            "completed_at": challenge.completed_at.isoformat() if challenge.completed_at else None,
            "time_spent": challenge.best_time or 0
        })
    
    return leaderboard
