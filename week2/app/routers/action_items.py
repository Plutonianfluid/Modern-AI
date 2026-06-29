from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemResponse,
    ExtractActionItemsRequest,
    ExtractActionItemsResponse,
    ExtractedActionItemResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services import extract as extract_service

router = APIRouter(prefix="/action-items", tags=["action-items"])


def _extract_and_save(
    payload: ExtractActionItemsRequest,
    extractor,
) -> ExtractActionItemsResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: int | None = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extractor(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractActionItemsResponse(
        note_id=note_id,
        items=[ExtractedActionItemResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    return _extract_and_save(payload, extract_service.extract_action_items)


@router.post("/extract-llm", response_model=ExtractActionItemsResponse)
def extract_llm(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    extractor = getattr(
        extract_service,
        "extract_action_items_llm",
        extract_service.extract_action_items,
    )
    return _extract_and_save(payload, extractor)


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: int | None = None) -> list[ActionItemResponse]:
    return [ActionItemResponse(**row) for row in db.list_action_items(note_id=note_id)]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    updated = db.mark_action_item_done(action_item_id, payload.done)
    if not updated:
        raise HTTPException(status_code=404, detail="action item not found")
    return MarkDoneResponse(id=action_item_id, done=payload.done)
