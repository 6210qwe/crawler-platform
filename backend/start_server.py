#!/usr/bin/env python3
"""
启动服务器，绕过SQLAlchemy的WMI问题
"""
import os
import sys

# 设置环境变量
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'
os.environ['PYTHONPATH'] = os.pathsep.join([os.getcwd(), os.environ.get('PYTHONPATH', '')])

# 导入并启动应用
if __name__ == "__main__":
    try:
        from app.main import app
        import uvicorn
        
        print("🚀 启动爬虫工具平台后端服务...")
        print("📊 数据库驱动架构已启用")
        print("🌐 访问地址: http://localhost:8000")
        print("📖 API文档: http://localhost:8000/docs")
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

