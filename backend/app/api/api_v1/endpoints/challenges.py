from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from sqlalchemy import func
import json
import random
from datetime import datetime

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, ChallengeSubmission
from app.models.exercise import Exercise
from app.schemas.challenge import ChallengeCreate, ChallengeMetaResponse, ChallengeSubmission as ChallengeSubmissionSchema, ChallengePageResponse
from app.services.exercise_service import ExerciseService
from app.challenge_validators.registry import get_validator_for_exercise

router = APIRouter()

def resolve_exercise_id(exercise_id_or_sort_order: int, db: Session) -> int:
    """解析exercise_id，支持通过ID或sort_order查找"""
    # 首先尝试通过ID查找
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id_or_sort_order).first()
    if exercise:
        return exercise.id
    
    # 如果通过ID找不到，尝试通过sort_order查找
    exercise = db.query(Exercise).filter(
        Exercise.sort_order == exercise_id_or_sort_order,
        Exercise.is_active == True
    ).first()
    if exercise:
        return exercise.id
    
    # 如果都找不到，返回原始值（让后续的错误处理来处理）
    return exercise_id_or_sort_order

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

def _honor_title(solved_count: int) -> str:
    tier = solved_count // 3
    if tier <= 0:
        return "新手入门"
    if tier == 1:
        return "初探江湖"
    if tier == 2:
        return "小有成就"
    if tier == 3:
        return "登堂入室"
    if tier == 4:
        return "炉火纯青"
    if tier == 5:
        return "登峰造极"
    return "传说宗师"

@router.get("/leaderboard")
async def get_leaderboard(
    sort_by: str = Query("score", regex="^(score|solved)$"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取全站用户聚合排行榜（按总分或解题数）。"""
    q = (
        db.query(
            User.id.label("user_id"),
            User.username,
            User.full_name,
            User.avatar_url,
            func.coalesce(func.sum(Challenge.score), 0).label("total_score"),
            func.count(Challenge.id).label("solved_count"),
            func.max(Challenge.completed_at).label("last_submission_at"),
        )
        .join(Challenge, Challenge.user_id == User.id)
        .filter(Challenge.is_completed == True)
        .group_by(User.id)
    )

    if sort_by == "solved":
        # 仅显示通过题数 > 1 的用户
        q = q.having(func.count(Challenge.id) > 1)
        q = q.order_by(func.count(Challenge.id).desc(), func.coalesce(func.sum(Challenge.score), 0).desc())
    else:
        # 仅显示积分 > 1 的用户
        q = q.having(func.coalesce(func.sum(Challenge.score), 0) > 1)
        q = q.order_by(func.coalesce(func.sum(Challenge.score), 0).desc(), func.count(Challenge.id).desc())

    rows = q.limit(limit).all()

    leaderboard = []
    for r in rows:
        leaderboard.append({
            "user_id": r.user_id,
            "username": r.username,
            "full_name": r.full_name,
            "avatar_url": r.avatar_url,
            "total_score": int(r.total_score or 0),
            "solved_count": int(r.solved_count or 0),
            "last_submission_at": r.last_submission_at.isoformat() if r.last_submission_at else None,
            "honor_title": _honor_title(int(r.solved_count or 0)),
        })

    return leaderboard

@router.get("/recent-completions")
async def get_recent_completions(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """最近通关记录，显示谁通过了哪一题。"""
    rows = (
        db.query(
            Challenge.id.label("challenge_id"),
            Challenge.completed_at,
            Challenge.score,
            User.id.label("user_id"),
            User.username,
            User.full_name,
            User.avatar_url,
            Exercise.id.label("exercise_id"),
            Exercise.title.label("exercise_title"),
        )
        .join(User, User.id == Challenge.user_id)
        .join(Exercise, Exercise.id == Challenge.exercise_id)
        .filter(Challenge.is_completed == True)
        .order_by(Challenge.completed_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "challenge_id": r.challenge_id,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "score": r.score or 0,
            "user_id": r.user_id,
            "username": r.username,
            "full_name": r.full_name,
            "avatar_url": r.avatar_url,
            "exercise_id": r.exercise_id,
            "exercise_title": r.exercise_title,
        }
        for r in rows
    ]

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
    # 解析exercise_id（支持通过ID或sort_order查找）
    actual_exercise_id = resolve_exercise_id(exercise_id, db)
    
    # 查找现有挑战
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == actual_exercise_id
    ).first()
    
    if not challenge:
        # 创建新挑战（一次性写入，后续仅做切片返回）
        numbers, total_sum = generate_challenge_numbers(current_user.id, actual_exercise_id)
        
        challenge = Challenge(
            user_id=current_user.id,
            exercise_id=actual_exercise_id,
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
    r: Optional[str] = Query(None, description="MD5参数，第一题需要"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取挑战页面数据"""
    if page_number < 1 or page_number > 100:
        raise HTTPException(status_code=400, detail="页面编号必须在1-100之间")
    
    # 解析exercise_id（支持通过ID或sort_order查找）
    actual_exercise_id = resolve_exercise_id(exercise_id, db)
    
    # 第一题需要MD5参数验证
    if actual_exercise_id == 1:
        if not r:
            raise HTTPException(status_code=400, detail="第一题需要携带r参数")
        
        # 验证MD5参数
        import hashlib
        import time
        
        # 获取当前时间戳
        current_timestamp = int(time.time())
        
        # 验证时间戳是否在合理范围内（5分钟内）
        # 尝试当前时间戳和前5分钟的时间戳
        md5_valid = False
        for i in range(6):  # 检查当前时间和前5分钟
            test_timestamp = current_timestamp - i * 60
            test_raw_string = str(test_timestamp) + 'spider'
            test_md5 = hashlib.md5(test_raw_string.encode('utf-8')).hexdigest()
            if r == test_md5:
                md5_valid = True
                break
        
        if not md5_valid:
            raise HTTPException(status_code=400, detail="MD5参数验证失败")
    
    # 查找挑战数据
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == actual_exercise_id
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

@router.get("/{exercise_id}/prepare")
async def prepare_challenge(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """返回本题所需的公开参数（nonce/seed/每日因子/版本等）"""
    # 解析exercise_id（支持通过ID或sort_order查找）
    actual_exercise_id = resolve_exercise_id(exercise_id, db)
    
    validator = get_validator_for_exercise(actual_exercise_id)
    if validator:
        return validator.get_public_params(user=current_user, exercise_id=actual_exercise_id)
    # 默认返回空参数
    return {"version": "1.0.0"}

@router.post("/submit")
async def submit_challenge(
    submission: ChallengeSubmissionSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交挑战答案"""
    # 解析exercise_id（支持通过ID或sort_order查找）
    actual_exercise_id = resolve_exercise_id(submission.exercise_id, db)
    
    # 查找挑战数据
    challenge = db.query(Challenge).filter(
        Challenge.user_id == current_user.id,
        Challenge.exercise_id == actual_exercise_id
    ).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    # 通过校验器验证（如存在）
    is_correct = submission.answer == challenge.total_sum
    validator = get_validator_for_exercise(actual_exercise_id)
    if validator:
        try:
            public_params = {}
            is_correct = validator.validate(
                submission=submission,
                user=current_user,
                exercise_id=actual_exercise_id,
                public_params=public_params,
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"校验失败: {str(e)}")
    
    # 记录提交
    submission_record = ChallengeSubmission(
        challenge_id=challenge.id,
        user_id=current_user.id,
        exercise_id=actual_exercise_id,
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
        exercise = db.query(Exercise).filter(Exercise.id == actual_exercise_id).first()
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

