from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., max_length=10000)

class NoteCreate(NoteBase):
    id: Optional[str] = None  # Frontend'den gelen ID'yi kabul et

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, max_length=10000)

class NoteResponse(NoteBase):
    id: str
    ownerUid: str = Field(alias="owner_uid")
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")
    dirty: bool = False
    deleted: bool = False
    hasTodos: bool = False
    todos: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserResponse(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None

    class Config:
        from_attributes = True

class NoteSummaryRequest(BaseModel):
    content: str = Field(..., min_length=5, max_length=10000)

class NoteSummaryResponse(BaseModel):
    summary: str
    keyPoints: list[str] = Field(default_factory=list)
    wordCount: int
    originalWordCount: int

class TodoExtractionRequest(BaseModel):
    content: str = Field(..., min_length=5, max_length=10000)

class TodoExtractionResponse(BaseModel):
    hasTodos: bool
    todos: list[str] = Field(default_factory=list)
    originalContent: str