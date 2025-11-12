from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import models

def get_indexes(db: Session):
    return db.query(models.VectorIndex).order_by(models.VectorIndex.created_at.desc()).all()

def create_index(db: Session, name: str, dimension: int):
    exists = db.query(models.VectorIndex).filter(models.VectorIndex.name == name).first()
    if exists:
        return None
    idx = models.VectorIndex(name=name, dimension=dimension, created_at=datetime.utcnow())
    db.add(idx)
    db.commit()
    db.refresh(idx)
    return idx

def delete_index(db: Session, name: str):
    idx = db.query(models.VectorIndex).filter(models.VectorIndex.name == name).first()
    if not idx:
        return False
    db.delete(idx)
    db.commit()
    return True

def add_file_metadata(db: Session, index_name: str, filename: str, size_bytes: int = 0):
    f = models.IndexFile(id=uuid.uuid4(), index_name=index_name, filename=filename, size_bytes=size_bytes, uploaded_at=datetime.utcnow(), status="uploaded")
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

def delete_file(db: Session, file_id: str):
    f = db.query(models.IndexFile).filter(models.IndexFile.id == file_id).first()
    if not f:
        return False
    db.delete(f)
    db.commit()
    return True
