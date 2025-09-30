from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, exercises, study_notes, challenges, exercises_new

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(exercises_new.router, prefix="/exercises", tags=["题目管理"])
api_router.include_router(study_notes.router, prefix="/notes", tags=["学习笔记"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["挑战赛"])

