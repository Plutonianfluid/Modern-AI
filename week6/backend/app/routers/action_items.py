from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemPage, ActionItemRead, BulkCompleteRequest

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=ActionItemPage)
def list_items(
    completed: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> ActionItemPage:
    query = select(ActionItem)
    count_query = select(func.count()).select_from(ActionItem)
    if completed is not None:
        query = query.where(ActionItem.completed == completed)
        count_query = count_query.where(ActionItem.completed == completed)
    total = db.scalar(count_query) or 0
    rows = db.execute(
        query.order_by(ActionItem.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).scalars()
    return ActionItemPage(
        items=[ActionItemRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete", response_model=list[ActionItemRead])
def bulk_complete(
    payload: BulkCompleteRequest, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    if len(set(payload.ids)) != len(payload.ids):
        raise HTTPException(status_code=400, detail="Duplicate action item IDs")
    items = db.execute(select(ActionItem).where(ActionItem.id.in_(payload.ids))).scalars().all()
    found = {item.id for item in items}
    missing = [item_id for item_id in payload.ids if item_id not in found]
    if missing:
        raise HTTPException(status_code=404, detail=f"Action items not found: {missing}")
    for item in items:
        item.completed = True
    db.flush()
    return [ActionItemRead.model_validate(item) for item in items]


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)
