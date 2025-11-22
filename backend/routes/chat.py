from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from services import chat_service
import schema
from utils.security import get_current_user

router = APIRouter(prefix="/api/chats", tags=["Chat"])

@router.get("/", response_model=list[schema.ChatOut])
def list_chats(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return chat_service.get_all_chats(db, user_id=str(current_user.id))

@router.post("/", response_model=schema.ChatOut)
def create_chat(model: str = Form("gpt-4o"), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return chat_service.create_chat(db, model, user_id=str(current_user.id))

@router.post("/{chat_id}/messages", response_model=schema.ChatOut)
def send_message(chat_id: str, content: str = Form(...),index_name = Form(...) ,db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = str(current_user.id)
    # Lấy index_name nếu cần (ví dụ lấy theo user hoặc chat, hoặc truyền từ frontend)
    # Ux click index_name từ frontend
    index_name = index_name.strip()
    if not index_name:
        raise HTTPException(status_code=422, detail="Index name cannot be empty")
    # Gọi agent để lấy AI response thực tế
    chat = chat_service.send_message_with_agent(db, chat_id, content, user_id=user_id, index_name=index_name)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    # Lưu memory vào Redis
    messages = [
        {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in chat.messages
    ]
    chat_service.save_chat_memory(user_id, chat_id, messages)
    return chat

@router.delete("/{chat_id}")
def delete_chat(chat_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ok = chat_service.delete_chat(db, chat_id, user_id=str(current_user.id))
    if not ok:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Deleted"}

@router.get("/{chat_id}", response_model=schema.ChatOut)
def get_chat(chat_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    chat = chat_service.get_chat(db, chat_id, user_id=str(current_user.id))
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.put("/{chat_id}/rename", response_model=schema.ChatOut)
def rename_chat(chat_id: str, title: str = Form(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return chat_service.rename_chat(db, chat_id, title, user_id=str(current_user.id))


