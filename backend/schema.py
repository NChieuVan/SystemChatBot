from pydantic import BaseModel as PydanticBaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import UUID


# ============================
# Base model
# ============================
class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True


# ============================
# USER
# ============================
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID
    created_at: datetime


# ============================
# MESSAGE
# ============================
class MessageBase(BaseModel):
    role: str
    content: str


class MessageOut(MessageBase):
    id: UUID
    created_at: datetime


# ============================
# CHAT
# ============================
class ChatBase(BaseModel):
    title: Optional[str] = "New chat"
    model: Optional[str] = "gpt-4o"


class ChatOut(ChatBase):
    id: UUID
    created_at: datetime
    messages: Optional[List[MessageOut]] = []


# ============================
# VECTOR INDEX
# ============================
class IndexFileOut(BaseModel):
    id: UUID
    filename: str
    size_bytes: int
    uploaded_at: datetime
    status: str


class IndexOut(BaseModel):
    id: UUID
    name: str
    dimension: int
    created_at: datetime
    files: Optional[List[IndexFileOut]] = []


# ============================
# METADATA
# ============================
class MetadataOut(BaseModel):
    id: UUID
    key: str
    value: Optional[str]
    created_at: datetime
