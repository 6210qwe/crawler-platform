#!/usr/bin/env python3
"""
修复 sort_order 字段，确保第一题（按 id 排序的第一条）的 sort_order = 1
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.exercise import Exercise
from sqlalchemy import asc

def fix_sort_order():
    """修复 sort_order 字段"""
    db = SessionLocal()
    try:
        # 获取所有题目，按 id 排序
        exercises = db.query(Exercise).filter(Exercise.is_active == True).order_by(asc(Exercise.id)).all()
        
        print(f"找到 {len(exercises)} 个题目")
        
        # 更新 sort_order
        for i, exercise in enumerate(exercises, 1):
            old_sort_order = exercise.sort_order
            exercise.sort_order = i
            print(f"题目 {exercise.id}: sort_order {old_sort_order} -> {i}")
        
        db.commit()
        print("✅ sort_order 修复完成！")
        
        # 验证第一题
        first_exercise = db.query(Exercise).filter(Exercise.sort_order == 1).first()
        if first_exercise:
            print(f"✅ 第一题确认: ID={first_exercise.id}, sort_order={first_exercise.sort_order}")
        else:
            print("❌ 未找到第一题")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_sort_order()


