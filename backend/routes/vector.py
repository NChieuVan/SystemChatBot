from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import vector_service
import schema
from utils.security import get_current_user
router = APIRouter(prefix="/api/indexes", tags=["Vector"])

@router.get("/", response_model=list[schema.IndexOut])
def list_indexes(db: Session = Depends(get_db)):
    return vector_service.get_indexes(db)

@router.post("/", response_model=schema.IndexOut)
def create_index(name: str = Form(...), dimension: int = Form(1536), db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    # Validate name
    if not name or not name.strip():
        raise HTTPException(status_code=422, detail="Tên index không được để trống.")
    # Validate dimension
    if not isinstance(dimension, int) or dimension <= 0:
        raise HTTPException(status_code=422, detail="Dimension phải là số nguyên dương.")

    index = vector_service.create_index(db, name.strip(), dimension, user_id=str(current_user.id))
    if not index:
        raise HTTPException(status_code=400, detail="Index đã tồn tại cho user này.")
    return index

@router.delete("/{name}")
def delete_index(name: str, db: Session = Depends(get_db)):
    ok = vector_service.delete_index(db, name)
    if not ok:
        raise HTTPException(status_code=404, detail="Index not found")
    return {"message": "Index deleted"}
