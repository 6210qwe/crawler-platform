#!/usr/bin/env python3
"""
简化版启动脚本，避免SQLAlchemy WMI问题
"""
import os
import sys

# 设置环境变量避免WMI问题
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        # 直接导入main模块
        from app.main import app
        import uvicorn
        
        print("🚀 爬虫工具平台后端服务启动中...")
        print("📊 混合架构：数据库驱动 + 前端配置")
        print("🌐 服务地址: http://localhost:8000")
        print("📖 API文档: http://localhost:8000/docs")
        print("=" * 50)
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

