from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class NoteRead(ORMModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1)
    project_id: int | None = Field(default=None, gt=0)


class ActionItemRead(ORMModel):
    id: int
    description: str
    completed: bool
    project_id: int | None
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(BaseModel):
    description: str | None = Field(default=None, min_length=1)
    completed: bool | None = None
    project_id: int | None = Field(default=None, gt=0)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class ProjectRead(ORMModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
