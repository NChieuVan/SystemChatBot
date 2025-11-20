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
def send_message(chat_id: str, content: str = Form(...), db: Session = Depends(get_db)):
    chat = chat_service.send_message(db, chat_id, content)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
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


