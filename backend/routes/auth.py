from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from services import user_service
from utils.security import create_access_token

import models

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
def register(email: str = Form(...), password: str = Form(...), name: str = Form(None), db: Session = Depends(get_db)):
    u = user_service.create_user(db, email=email, password=password, name=name)
    if not u:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "Registered"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    u = user_service.authenticate(db, email, password)
    if not u:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(u.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/all_users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users