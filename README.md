# 爬虫逆向学习平台

一个现代化的爬虫逆向学习平台，支持用户注册、登录、学习案例管理和在线学习。

## 技术栈

### 后端
- **FastAPI** - 现代、高性能的Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 数据库
- **JWT** - 用户认证
- **Alembic** - 数据库迁移

### 前端
- **React 18** - 前端框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - CSS框架
- **React Router** - 路由管理

## 项目结构

```
crawler-reverse-platform/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic模型
│   │   └── services/       # 业务逻辑
│   ├── alembic/            # 数据库迁移
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # React组件
│   │   ├── pages/          # 页面组件
│   │   ├── services/       # API服务
│   │   └── utils/          # 工具函数
│   └── package.json        # Node.js依赖
└── docker-compose.yml      # 容器编排
```

## 快速开始

### 方式一：一键启动（推荐）
```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# Windows
start.bat
```

### 方式二：手动启动

#### 1. 启动数据库
```bash
docker-compose up -d
```

#### 2. 启动后端
```bash
cd backend
pip install -r requirements.txt
python init_db.py  # 初始化数据库
python run.py      # 启动后端服务
```

#### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 访问地址
- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API文档：http://localhost:8000/docs

## 功能特性

- 🔐 用户注册/登录
- 📚 学习案例管理
- 🎯 在线学习
- 📊 学习进度跟踪
- 📝 学习笔记
- 🎨 现代化UI设计

