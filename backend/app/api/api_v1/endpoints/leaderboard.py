from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db


router = APIRouter()


@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    # 直接读取视图 v_user_leaderboard（你已在DB创建）
    rows = db.execute("SELECT user_id, username, full_name, total_score, solved_count, last_submission_at FROM v_user_leaderboard").fetchall()
    return [
        {
            "user_id": r[0],
            "username": r[1],
            "full_name": r[2],
            "total_score": int(r[3]) if r[3] is not None else 0,
            "solved_count": int(r[4]) if r[4] is not None else 0,
            "last_submission_at": r[5],
        }
        for r in rows
    ]


