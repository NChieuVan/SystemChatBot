import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

# -------------------- USER --------------------
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chats = relationship("Chat", back_populates="user", cascade="all, delete")
    vector_indexes = relationship("VectorIndex", back_populates="user", cascade="all, delete")


# -------------------- CHAT --------------------
class Chat(Base):
    __tablename__ = "chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), default="New chat")
    model = Column(String(100), default="gpt-4o")
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="chats")

    messages = relationship("Message", back_populates="chat", cascade="all, delete")
    meta_info = relationship("Metadata", back_populates="chat", cascade="all, delete")  # ✅ renamed


# -------------------- MESSAGE --------------------
class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String(50), nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    chat = relationship("Chat", back_populates="messages")


# -------------------- VECTOR INDEX --------------------
class VectorIndex(Base):
    __tablename__ = "vector_indexes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    dimension = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="none")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="vector_indexes")

    files = relationship("IndexFile", back_populates="index", cascade="all, delete")


# -------------------- INDEX FILE --------------------
class IndexFile(Base):
    __tablename__ = "index_files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    size_bytes = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="ready")

    index_id = Column(UUID(as_uuid=True), ForeignKey("vector_indexes.id", ondelete="CASCADE"))
    index = relationship("VectorIndex", back_populates="files")


# -------------------- METADATA --------------------
class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    chat = relationship("Chat", back_populates="meta_info")  # ✅ renamed
