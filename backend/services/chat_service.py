import uuid
from datetime import datetime
from sqlalchemy.orm import Session,selectinload
import models
from fastapi import HTTPException
from utils.redis_client import redis_client
import json
from graph.agent import agent
from langchain_core.messages import HumanMessage

def get_all_chats(db: Session,user_id: str):
    chats = db.query(models.Chat).filter(models.Chat.user_id == user_id).options(selectinload(models.Chat.messages)).all()
    return chats 

def create_chat(db: Session, model: str = "gpt-4o", user_id: str = None):
    chat = models.Chat(id=uuid.uuid4(), title="New chat", model=model, created_at=datetime.utcnow(), user_id=user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def send_message(db: Session, chat_id: str, content: str, ai_response: str = None):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        return None
    msg_user = models.Message(id=uuid.uuid4(), role="user", content=content, chat_id=chat_id, created_at=datetime.utcnow())
    # Nếu có response từ AI thì lưu, nếu không thì lưu demo
    if ai_response is None:
        ai_response = f"({chat.model}) Demo trả lời: '{content}'"
    msg_bot = models.Message(id=uuid.uuid4(), role="assistant", content=ai_response, chat_id=chat_id, created_at=datetime.utcnow())
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

# Lưu lịch sử chat vào Redis theo user_id và chat_id
# Key: f"chat_memory:{user_id}:{chat_id}"
def save_chat_memory(user_id: str, chat_id: str, messages: list):
    key = f"chat_memory:{user_id}:{chat_id}"
    # Chỉ lưu 20 message gần nhất
    messages = messages[-20:]
    redis_client.set(key, json.dumps(messages), ex=60*60*24)  # TTL 1 ngày

def get_chat_memory(user_id: str, chat_id: str):
    key = f"chat_memory:{user_id}:{chat_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return []

def send_message_with_agent(db: Session, chat_id: str, content: str, user_id: str, index_name: str):
    # 1. Tạo state cho agent
    state = {"messages": [HumanMessage(content=content)]}
    # 2. Gọi agent để lấy response AI
    result = agent.invoke(state, user_id=user_id, chat_id=chat_id, index_name=index_name)
    ai_message = None
    for msg in result["messages"]:
        if hasattr(msg, "content"):
            ai_message = msg.content
    # 3. Lưu cả user message và AI response vào DB
    return send_message(db, chat_id, content, ai_response=ai_message)


