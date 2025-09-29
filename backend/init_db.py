#!/usr/bin/env python3
"""
初始化数据库脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.database import Base
from app.core.config import settings
from app.models import *
import pymysql

def init_database():
    """初始化数据库"""
    print("🗄️ 正在初始化数据库...")
    # 确保数据库存在（通过PyMySQL直连MySQL服务创建数据库）
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_SERVER,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            port=settings.MYSQL_PORT,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        print(f"✅ 已确保数据库存在: {settings.MYSQL_DB}")
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        raise

    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("✅ 数据库初始化完成！")

if __name__ == "__main__":
    init_database()

