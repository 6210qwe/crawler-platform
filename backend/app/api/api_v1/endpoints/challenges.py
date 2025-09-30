from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union
import json
import random
from datetime import datetime

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, ChallengeSubmission
from app.models.exercise import Exercise
from app.schemas.challenge import ChallengeCreate, ChallengeMetaResponse, ChallengeSubmission as ChallengeSubmissionSchema, ChallengePageResponse

router = APIRouter()

def generate_challenge_numbers(user_id: int, exercise_id: int) -> tuple[List[List[int]], int]:
    """生成用户特定的挑战数字"""
    numbers: List[List[int]] = []
    total_sum = 0
    
    for page in range(100):
        # 为每一页创建确定性的随机源，避免顺序数字
        rng = random.Random(f"user:{user_id}|ex:{exercise_id}|page:{page}")
        # 在 1..200 中采样 10 个互不相同的数字，顺序由随机源决定
        page_numbers = rng.sample(range(1, 201), 10)
        total_sum += sum(page_numbers)
        numbers.append(page_numbers)
    
    return numbers, total_sum

def _expected_page_numbers(user_id: int, exercise_id: int, page_zero_based: int) -> List[int]:
    rng = random.Random(f"user:{user_id}|ex:{exercise_id}|page:{page_zero_based}")
    return rng.sample(range(1, 201), 10)

def ensure_challenge_up_to_date(challenge: Challenge, db: Session) -> tuple[list[list[int]], int]:
    """如果旧数据与新规则不一致，则重新生成并持久化。返回(numbers, total_sum)。"""
    numbers = json.loads(challenge.numbers_data)
    if not numbers or not isinstance(numbers, list) or not isinstance(numbers[0], list):
        new_numbers, new_total = generate_challenge_numbers(challenge.user_id, challenge.exercise_id)
        challenge.numbers_data = json.dumps(new_numbers)
        challenge.total_sum = new_total
        db.add(challenge)
        db.commit()
        return new_numbers, new_total

    # 对比第 0 页是否符合新规则
    expected_first = _expected_page_numbers(challenge.user_id, challenge.exercise_id, 0)
    if numbers[0] != expected_first:
        new_numbers, new_total = generate_challenge_numbers(challenge.user_id, challenge.exercise_id)
        challenge.numbers_data = json.dumps(new_numbers)
        challenge.total_sum = new_total
        db.add(challenge)
        db.commit()
        return new_numbers, new_total

    return numbers, challenge.total_sum

@router.get("/progress")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户挑战进度（放在可变路径前，避免被 /{exercise_id} 吃掉）"""
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
    """获取挑战排行榜（放在可变路径前，避免被 /{exercise_id} 吃掉）"""
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

@router.get("/leaderboard/{exercise_id}")
async def get_leaderboard_by_exercise(
    exercise_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """根据题目获取挑战排行榜（兼容前端路径）"""
    return await get_leaderboard(exercise_id=exercise_id, limit=limit, db=db)  # type: ignore

@router.get("/{exercise_id}", response_model=Union[ChallengeMetaResponse, ChallengePageResponse])
async def get_challenge(
    exercise_id: int,
    page: Optional[int] = Query(None, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取挑战元信息或单页数据。
    - 不带 page: 返回元信息（不含 numbers）
    - 带 page: 仍返回元信息（前端随后用 /page/{page_number} 或 ?page= 获取数据）
    兼容性：暂保持 /page/{page_number} 端点。
    """
    # 查找现有挑战
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == exercise_id
    ).first()
    
    if not challenge:
        # 创建新挑战（一次性写入，后续仅做切片返回）
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
        # 旧数据兼容：如与新规则不一致则重建
        ensure_challenge_up_to_date(challenge, db)

    total_pages = 100

    # 如果携带 page 参数，则返回对应页的数据
    if page is not None:
        # 旧数据兼容：如与新规则不一致则重建
        numbers, _ = ensure_challenge_up_to_date(challenge, db)
        page_numbers = numbers[page - 1]
        return ChallengePageResponse(
            page_number=page,
            numbers=page_numbers,
            start_index=(page - 1) * 10 + 1,
            end_index=page * 10
        )

    # 默认仅返回元信息，避免回传 1000 条
    return ChallengeMetaResponse(
        id=challenge.id,
        user_id=challenge.user_id,
        exercise_id=challenge.exercise_id,
        total_sum=challenge.total_sum,
        is_completed=challenge.is_completed,
        completed_at=challenge.completed_at,
        attempts=challenge.attempts,
        best_time=challenge.best_time,
        score=challenge.score,
        total_pages=total_pages
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

        # 同步更新题目统计：首次通关才累计成功人数
        exercise = db.query(Exercise).filter(Exercise.id == submission.exercise_id).first()
        if exercise:
            exercise.success_count = (exercise.success_count or 0) + 1
            exercise.attempt_count = (exercise.attempt_count or 0) + 1
            db.add(exercise)
    
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
