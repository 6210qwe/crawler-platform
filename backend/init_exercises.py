#!/usr/bin/env python3
"""
初始化题目数据到数据库
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.exercise import Exercise

# 创建所有表
Base.metadata.create_all(bind=engine)

# 题目数据
exercises_data = [
    {
        "title": "字体反爬之基础",
        "description": "识别并绕过基础字体反爬虫技术",
        "difficulty": "初级",
        "challenge_points": "字体文件分析、字符映射关系、字体替换技术",
        "tags": ["字体反爬", "字体映射", "字符识别"],
        "points": 10,
        "sort_order": 1
    },
    {
        "title": "动态字体之变幻",
        "description": "处理动态生成的字体文件",
        "difficulty": "初级",
        "challenge_points": "动态字体分析、字符编码规律、字体缓存机制",
        "tags": ["动态字体", "字体生成", "字符映射"],
        "points": 15,
        "sort_order": 2
    },
    {
        "title": "字体加密之迷雾",
        "description": "破解加密的字体文件",
        "difficulty": "中级",
        "challenge_points": "字体加密算法分析、密钥提取、解密实现",
        "tags": ["字体加密", "加密算法", "字体解密"],
        "points": 25,
        "sort_order": 3
    },
    {
        "title": "多字体混淆之复杂",
        "description": "处理多种字体混合使用的反爬",
        "difficulty": "中级",
        "challenge_points": "多字体识别、字体切换逻辑、字符对应关系",
        "tags": ["多字体", "字体混淆", "混合字体"],
        "points": 30,
        "sort_order": 4
    },
    {
        "title": "字体变形之扭曲",
        "description": "识别经过变形的字体字符",
        "difficulty": "中级",
        "challenge_points": "字体变形算法、字符特征提取、OCR识别优化",
        "tags": ["字体变形", "字符识别", "图像处理"],
        "points": 35,
        "sort_order": 5
    },
    {
        "title": "Cookie基础加密",
        "description": "识别并破解基础Cookie加密",
        "difficulty": "初级",
        "challenge_points": "Cookie结构分析、加密算法识别、解密实现",
        "tags": ["Cookie加密", "基础加密", "Cookie解析"],
        "points": 12,
        "sort_order": 6
    },
    {
        "title": "Cookie时间戳验证",
        "description": "绕过Cookie时间戳验证",
        "difficulty": "初级",
        "challenge_points": "时间戳算法、时间同步、Cookie伪造技术",
        "tags": ["时间戳", "时间验证", "Cookie伪造"],
        "points": 15,
        "sort_order": 7
    },
    {
        "title": "AES标准加密",
        "description": "破解AES标准加密算法",
        "difficulty": "初级",
        "challenge_points": "AES算法分析、密钥提取、解密实现",
        "tags": ["AES", "标准加密", "对称加密"],
        "points": 15,
        "sort_order": 8
    },
    {
        "title": "RSA非对称加密",
        "description": "破解RSA非对称加密",
        "difficulty": "初级",
        "challenge_points": "RSA算法分析、密钥分解、私钥提取",
        "tags": ["RSA", "非对称加密", "公钥密码"],
        "points": 18,
        "sort_order": 9
    },
    {
        "title": "Webpack基础分析",
        "description": "分析Webpack打包的JavaScript代码",
        "difficulty": "初级",
        "challenge_points": "Webpack结构分析、模块解析、代码还原",
        "tags": ["Webpack", "模块打包", "代码分析"],
        "points": 15,
        "sort_order": 10
    }
]

def init_exercises():
    """初始化题目数据"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(Exercise).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 道题目，跳过初始化")
            return
        
        # 插入题目数据
        for exercise_data in exercises_data:
            exercise = Exercise(
                title=exercise_data["title"],
                description=exercise_data["description"],
                difficulty=exercise_data["difficulty"],
                challenge_points=exercise_data["challenge_points"],
                tags=json.dumps(exercise_data["tags"], ensure_ascii=False),
                points=exercise_data["points"],
                sort_order=exercise_data["sort_order"],
                is_active=True
            )
            db.add(exercise)
        
        db.commit()
        print(f"成功初始化 {len(exercises_data)} 道题目")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_exercises()
