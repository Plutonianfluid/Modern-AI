from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePage, NoteRead, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=NotePage)
def list_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> NotePage:
    total = db.scalar(select(func.count()).select_from(Note)) or 0
    rows = db.execute(
        select(Note).order_by(Note.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).scalars()
    return NotePage(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search", response_model=NotePage)
@router.get("/search/", response_model=NotePage, include_in_schema=False)
def search_notes(
    q: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: str = Query("created_desc", pattern="^(created_desc|title_asc)$"),
    db: Session = Depends(get_db),
) -> NotePage:
    query = select(Note)
    count_query = select(func.count()).select_from(Note)
    if q.strip():
        pattern = f"%{q.strip()}%"
        condition = or_(Note.title.ilike(pattern), Note.content.ilike(pattern))
        query = query.where(condition)
        count_query = count_query.where(condition)
    ordering = (Note.title.asc(), Note.id.asc()) if sort == "title_asc" else (Note.id.desc(),)
    total = db.scalar(count_query) or 0
    rows = db.execute(
        query.order_by(*ordering).offset((page - 1) * page_size).limit(page_size)
    ).scalars()
    return NotePage(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = payload.title
    note.content = payload.content
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)
