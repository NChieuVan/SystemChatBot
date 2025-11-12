from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from services import chat_service
import schema

router = APIRouter(prefix="/api/chats", tags=["Chat"])

@router.get("/", response_model=list[schema.ChatOut])
def list_chats(db: Session = Depends(get_db)):
    return chat_service.get_all_chats(db)

@router.post("/", response_model=schema.ChatOut)
def create_chat(model: str = Form("gpt-4o"), db: Session = Depends(get_db)):
    return chat_service.create_chat(db, model)

@router.post("/{chat_id}/messages", response_model=schema.ChatOut)
def send_message(chat_id: str, content: str = Form(...), db: Session = Depends(get_db)):
    chat = chat_service.send_message(db, chat_id, content)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.delete("/{chat_id}")
def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    ok = chat_service.delete_chat(db, chat_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Deleted"}
