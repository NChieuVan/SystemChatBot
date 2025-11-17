from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from utils.security import get_current_user


router = APIRouter(prefix="/api/fileindex", tags=["FileIndex"])

@router.get("/{index_name}/files")
def list_files_in_index(index_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    idx = db.query(models.VectorIndex).filter(
        models.VectorIndex.name == index_name.strip(),
        models.VectorIndex.user_id == current_user.id
    ).first()
    if not idx:
        raise HTTPException(status_code=404, detail="Index not found in your account")
    
    files = db.query(models.IndexFile).filter(
        models.IndexFile.index_id == idx.id
    ).all()
    
    return [
        {
            "file_id": str(f.id),
            "filename": f.filename,
            "size_bytes": f.size_bytes,
            "uploaded_at": f.uploaded_at,
            "status": f.status
        } for f in files
    ]

@router.delete("/{index_name}/files/{file_id}")
def delete_file_from_index(index_name: str, file_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    idx = db.query(models.VectorIndex).filter(
        models.VectorIndex.name == index_name.strip(),
        models.VectorIndex.user_id == current_user.id
    ).first()
    if not idx:
        raise HTTPException(status_code=404, detail="Index not found in your account")
    
    file = db.query(models.IndexFile).filter(
        models.IndexFile.id == file_id,
        models.IndexFile.index_id == idx.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found in the specified index")
    
    db.delete(file)
    db.commit()
    
    return {"detail": "File deleted successfully"}