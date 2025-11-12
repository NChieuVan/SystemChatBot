from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# -------------------- USER --------------------
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    created_at: datetime
    class Config:
        orm_mode = True


# -------------------- MESSAGE --------------------
class MessageBase(BaseModel):
    role: str
    content: str

class MessageOut(MessageBase):
    id: str
    created_at: datetime
    class Config:
        orm_mode = True


# -------------------- CHAT --------------------
class ChatBase(BaseModel):
    title: Optional[str] = "New chat"
    model: Optional[str] = "gpt-4o"

class ChatOut(ChatBase):
    id: str
    created_at: datetime
    messages: Optional[List[MessageOut]] = []
    class Config:
        orm_mode = True


# -------------------- VECTOR INDEX --------------------
class IndexFileOut(BaseModel):
    id: str
    filename: str
    size_bytes: int
    uploaded_at: datetime
    status: str
    class Config:
        orm_mode = True

class IndexOut(BaseModel):
    id: str
    name: str
    dimension: int
    created_at: datetime
    files: Optional[List[IndexFileOut]] = []
    class Config:
        orm_mode = True


# -------------------- METADATA --------------------
class MetadataOut(BaseModel):
    id: str
    key: str
    value: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True
