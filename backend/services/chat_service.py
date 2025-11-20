import uuid
from datetime import datetime
from sqlalchemy.orm import Session,selectinload
import models
from fastapi import HTTPException
def get_all_chats(db: Session,user_id: str):
    chats = db.query(models.Chat).filter(models.Chat.user_id == user_id).options(selectinload(models.Chat.messages)).all()
    return chats 

def create_chat(db: Session, model: str = "gpt-4o", user_id: str = None):
    chat = models.Chat(id=uuid.uuid4(), title="New chat", model=model, created_at=datetime.utcnow(), user_id=user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def send_message(db: Session, chat_id: str, content: str):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        return None
    msg_user = models.Message(id=uuid.uuid4(), role="user", content=content, chat_id=chat_id, created_at=datetime.utcnow())
    msg_bot = models.Message(id=uuid.uuid4(), role="assistant", content=f"({chat.model}) Demo trả lời: '{content}'", chat_id=chat_id, created_at=datetime.utcnow())
    db.add_all([msg_user, msg_bot])
    db.commit()
    db.refresh(chat)
    return chat

def delete_chat(db: Session, chat_id: str,user_id: str):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id, models.Chat.user_id==user_id).first()
    if not chat:
        return False
    db.delete(chat)
    db.commit()
    return True

def get_chat(db: Session, chat_id: str, user_id: str):
    return db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.user_id == user_id
    ).first()

def rename_chat(db: Session, chat_id: str, title: str, user_id: str):
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.user_id == user_id
    ).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat.title = title
    db.commit()
    db.refresh(chat)
    return chat


