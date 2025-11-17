from datetime import datetime
import uuid
from sqlalchemy.orm import Session,relationship
import models
from services import pinecone_service

def get_indexes(db: Session, user_id: str):
    # return db.query(models.VectorIndex).filter(models.VectorIndex.user_id == uuid.UUID(user_id)).all()
    indexes = db.query(models.VectorIndex).filter(models.VectorIndex.user_id == user_id).all()
    return [
    {
        "id": str(idx.id),
        "name": idx.name,
        "dimension": idx.dimension,
        "created_at": idx.created_at
    } for idx in indexes
    ]


def create_index(db: Session, name: str, dimension: int,user_id: str):
    exists = db.query(models.VectorIndex).filter(models.VectorIndex.name == name,
                                                 models.VectorIndex.user_id ==user_id ).first()
    if exists:
        return None
    idx = models.VectorIndex(name=name, 
                             dimension=dimension, 
                             created_at=datetime.utcnow(), 
                             user_id=user_id, 
                             status="creating")
    db.add(idx)
    db.commit()
    db.refresh(idx)
    # Create index in Pinecone
    result = pinecone_service.create_pinecone_index(name, dimension)
    if result.get("status") == "ready":
        idx.status = "ready"
    else:
        idx.status = "error"
    db.commit()
    db.refresh(idx)
    return idx

def delete_index(db: Session, name: str, user_id: str):
    """Delete index by name and user_id.
    - Returns True if deleted, \n\tFalse if not found.
    """
    exists = db.query(models.VectorIndex).filter(models.VectorIndex.name == name,
                                              models.VectorIndex.user_id == user_id).first()
    if not exists:
        return False
    # Delete from Pinecone
    result =  pinecone_service.delete_pinecone_index(name)
    if result.get("status") != "deleted":
        return False
    db.delete(exists)
    db.commit()
    return True

def add_file_metadata(db: Session, index_id: str, filename: str, size_bytes: int = 0):
    f = models.IndexFile(id=uuid.uuid4(), index_id = index_id, filename=filename, size_bytes=size_bytes, uploaded_at=datetime.utcnow(), status="uploaded")
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
