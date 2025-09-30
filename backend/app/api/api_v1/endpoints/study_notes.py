from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_user_optional, get_current_user
from app.models.user import User
from app.schemas.study_note import StudyNote, StudyNoteCreate, StudyNoteUpdate
from app.services.study_note_service import StudyNoteService


router = APIRouter()


@router.get("/", response_model=List[StudyNote])
@router.get("", response_model=List[StudyNote])
def list_notes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    service = StudyNoteService(db)
    if current_user:
        return service.list(current_user.id, skip=skip, limit=limit)
    else:
        # 未登录时返回空列表
        return []


@router.post("/", response_model=StudyNote)
@router.post("", response_model=StudyNote)
def create_note(
    data: StudyNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudyNoteService(db)
    return service.create(current_user.id, data)


@router.get("/{note_id}", response_model=StudyNote)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudyNoteService(db)
    note = service.get(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note


@router.put("/{note_id}", response_model=StudyNote)
def update_note(
    note_id: int,
    data: StudyNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudyNoteService(db)
    note = service.update(note_id, current_user.id, data)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudyNoteService(db)
    ok = service.soft_delete(note_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return {"success": True}


