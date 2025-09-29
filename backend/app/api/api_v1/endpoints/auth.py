from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """用户注册"""
    user_service = UserService(db)
    
    # 检查用户名是否已存在
    if user_service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if user_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="邮箱已存在"
        )
    
    # 创建用户
    user = user_service.create_user(user_data)
    return user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None
):
    """用户登录"""
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    # 设置 HttpOnly Cookie（本地测试 secure=False，生产需True并配合 HTTPS）
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    return {"user": UserSchema.model_validate(user)}

@router.get("/me", response_model=UserSchema)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """从Cookie中获取当前用户信息"""
    from jose import jwt, JWTError

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效凭据")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效凭据")

    user_service = UserService(db)
    user = user_service.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


@router.post("/logout")
def logout(response: Response):
    """清除登录Cookie"""
    response.delete_cookie("access_token", path="/")
    return {"message": "已退出登录"}
