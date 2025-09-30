#!/usr/bin/env python3
"""
删除exercises表
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def delete_exercises_table():
    """删除exercises表"""
    with engine.connect() as conn:
        # 先删除外键约束
        conn.execute(text("DROP TABLE IF EXISTS exercise_submissions"))
        conn.execute(text("DROP TABLE IF EXISTS challenges"))
        conn.execute(text("DROP TABLE IF EXISTS challenge_submissions"))
        # 再删除主表
        conn.execute(text("DROP TABLE IF EXISTS exercises"))
        conn.commit()
        print("所有相关表已删除")

if __name__ == "__main__":
    delete_exercises_table()
