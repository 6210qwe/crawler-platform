from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.study_note import StudyNote
from app.schemas.study_note import StudyNoteCreate, StudyNoteUpdate


class StudyNoteService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: StudyNoteCreate) -> StudyNote:
        note = StudyNote(
            user_id=user_id,
            title=data.title,
            content_html=data.content_html,
            content_text=data.content_text,
            tags=data.tags,
            is_private=data.is_private,
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note_id: int, user_id: int, data: StudyNoteUpdate) -> Optional[StudyNote]:
        note = self.db.query(StudyNote).filter(StudyNote.id == note_id, StudyNote.user_id == user_id).first()
        if not note:
            return None
        update_data = data.dict(exclude_unset=True)
        for k, v in update_data.items():
            setattr(note, k, v)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get(self, note_id: int, user_id: int) -> Optional[StudyNote]:
        note = self.db.query(StudyNote).filter(StudyNote.id == note_id, StudyNote.user_id == user_id).first()
        if note:
            # 增加阅读次数
            note.view_count += 1
            self.db.commit()
        return note

    def list(self, user_id: int, skip: int = 0, limit: int = 20) -> List[StudyNote]:
        return (
            self.db.query(StudyNote)
            .filter(StudyNote.user_id == user_id, StudyNote.deleted_at.is_(None))
            .order_by(StudyNote.updated_at.desc(), StudyNote.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def soft_delete(self, note_id: int, user_id: int) -> bool:
        note = self.get(note_id, user_id)
        if not note:
            return False
        from sqlalchemy.sql import func
        note.deleted_at = func.now()
        self.db.commit()
        return True


