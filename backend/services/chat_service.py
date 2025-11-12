import uuid
from datetime import datetime
from sqlalchemy.orm import Session
import models

def get_all_chats(db: Session):
    return db.query(models.Chat).order_by(models.Chat.created_at.desc()).all()

def create_chat(db: Session, model: str = "gpt-4o"):
    chat = models.Chat(id=uuid.uuid4(), title="New chat", model=model, created_at=datetime.utcnow())
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

def delete_chat(db: Session, chat_id: str):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        return False
    db.delete(chat)
    db.commit()
    return True
