from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.services.user_service import UserService
from app.api.api_v1.endpoints.auth import get_current_user as get_current_user_dep

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """获取用户列表"""
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """获取指定用户信息"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep)
):
    """更新用户信息"""
    # 只有用户本人或管理员可以更新
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="没有权限修改此用户信息"
        )
    
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    return user

