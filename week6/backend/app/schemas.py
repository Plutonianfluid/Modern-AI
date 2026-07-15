from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)

    @field_validator("title", "content")
    @classmethod
    def reject_whitespace(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class NoteUpdate(NoteCreate):
    pass


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=2_000)

    @field_validator("description")
    @classmethod
    def reject_whitespace(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class BulkCompleteRequest(BaseModel):
    ids: list[int] = Field(min_length=1)


class NotePage(BaseModel):
    items: list[NoteRead]
    total: int
    page: int
    page_size: int


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


class ActionItemPage(BaseModel):
    items: list[ActionItemRead]
    total: int
    page: int
    page_size: int
