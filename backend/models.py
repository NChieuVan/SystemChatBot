import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime,
    ForeignKey, Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ======================================================
# 🧑 USER MODEL
# ======================================================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Quan hệ: 1 user có nhiều chat
    chats = relationship("Chat", back_populates="user", cascade="all, delete")


# ======================================================
# 💬 CHAT MODEL
# ======================================================
class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), default="New chat")
    model = Column(String(100), default="gpt-4o")
    created_at = Column(DateTime, default=datetime.utcnow)

    # FK
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # Quan hệ: 1 chat có nhiều message
    messages = relationship("Message", back_populates="chat", cascade="all, delete")
    user = relationship("User", back_populates="chats")


# ======================================================
# 💬 MESSAGE MODEL
# ======================================================
class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String(50), nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # FK
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    chat = relationship("Chat", back_populates="messages")


# ======================================================
# 📂 VECTOR INDEX (PINECONE) MODEL
# ======================================================
class VectorIndex(Base):
    __tablename__ = "vector_indexes"

    name = Column(String(255), primary_key=True)
    dimension = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    files = relationship("IndexFile", back_populates="index", cascade="all, delete")


# ======================================================
# 📄 FILE TRONG MỖI INDEX
# ======================================================
class IndexFile(Base):
    __tablename__ = "index_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    size_bytes = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="ready")

    # FK
    index_name = Column(String(255), ForeignKey("vector_indexes.name", ondelete="CASCADE"))
    index = relationship("VectorIndex", back_populates="files")


# ======================================================
# 📊 METADATA (Lưu thêm thông tin phụ)
# ======================================================
class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=True)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
