@echo off
chcp 65001 >nul

echo 🚀 启动爬虫逆向练习题平台...

REM 检查Docker是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未运行，请先启动Docker
    pause
    exit /b 1
)

REM 启动数据库和Redis
echo 📦 启动数据库和Redis...
docker-compose up -d

REM 等待数据库启动
echo ⏳ 等待数据库启动...
timeout /t 10 /nobreak >nul

REM 安装后端依赖
echo 📦 安装后端依赖...
cd backend
pip install -r requirements.txt

REM 运行数据库迁移
echo 🗄️ 运行数据库迁移...
alembic upgrade head

REM 启动后端服务
echo 🔧 启动后端服务...
start "Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 安装前端依赖
echo 📦 安装前端依赖...
cd ..\frontend
npm install

REM 启动前端服务
echo 🎨 启动前端服务...
start "Frontend" cmd /k "npm run dev"

echo ✅ 平台启动完成！
echo 🌐 前端地址: http://localhost:3000
echo 🔧 后端地址: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs

pause

