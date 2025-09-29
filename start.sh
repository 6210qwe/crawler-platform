#!/bin/bash

# 爬虫逆向练习题平台启动脚本

echo "🚀 启动爬虫逆向练习题平台..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 启动数据库和Redis
echo "📦 启动数据库和Redis..."
docker-compose up -d

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 10

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
pip install -r requirements.txt

# 运行数据库迁移
echo "🗄️ 运行数据库迁移..."
alembic upgrade head

# 启动后端服务
echo "🔧 启动后端服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 安装前端依赖
echo "📦 安装前端依赖..."
cd ../frontend
npm install

# 启动前端服务
echo "🎨 启动前端服务..."
npm run dev &
FRONTEND_PID=$!

echo "✅ 平台启动完成！"
echo "🌐 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait

