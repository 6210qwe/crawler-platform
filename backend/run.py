#!/usr/bin/env python3
"""
爬虫逆向练习题平台后端启动脚本
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    # 使用导入字符串以启用 reload
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

