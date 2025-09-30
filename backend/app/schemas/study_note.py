from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class StudyNoteBase(BaseModel):
    title: str
    content_html: str
    content_text: Optional[str] = None
    tags: Optional[List[str]] = None
    is_private: bool = True


class StudyNoteCreate(StudyNoteBase):
    pass


class StudyNoteUpdate(BaseModel):
    title: Optional[str] = None
    content_html: Optional[str] = None
    content_text: Optional[str] = None
    tags: Optional[List[str]] = None
    is_private: Optional[bool] = None


class StudyNoteInDBBase(StudyNoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudyNote(StudyNoteInDBBase):
    pass


