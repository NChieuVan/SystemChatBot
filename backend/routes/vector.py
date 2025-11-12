from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import vector_service
import schema

router = APIRouter(prefix="/api/indexes", tags=["Vector"])

@router.get("/", response_model=list[schema.IndexOut])
def list_indexes(db: Session = Depends(get_db)):
    return vector_service.get_indexes(db)

@router.post("/", response_model=schema.IndexOut)
def create_index(name: str = Form(...), dimension: int = Form(1536), db: Session = Depends(get_db)):
    index = vector_service.create_index(db, name, dimension)
    if not index:
        raise HTTPException(status_code=400, detail="Index already exists")
    return index

@router.delete("/{name}")
def delete_index(name: str, db: Session = Depends(get_db)):
    ok = vector_service.delete_index(db, name)
    if not ok:
        raise HTTPException(status_code=404, detail="Index not found")
    return {"message": "Index deleted"}
