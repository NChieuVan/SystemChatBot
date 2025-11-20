from fastapi import APIRouter,Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from database import get_db
import models
from utils.security import get_current_user
from minio_client import minio_client, MINIO_BUCKET
from services.pinecone_service import delete_vectors_by_ids

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
async def delete_file_from_index(index_name: str, file_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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
    # Delete file from MinIO
    try:
        result = await run_in_threadpool(
            minio_client.remove_object,
            MINIO_BUCKET,
            f"{idx.name}_{file.filename}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file from storage: {e}")
    
    # Check if status file is uploaded then delete database, if status is embedded then query models.FileVectorMap and delete vectors from Pinecone and database
    if file.status == "uploaded":
        # Just delete metadata from DB
        db.delete(file)
        db.commit()
        return {"detail": "File deleted successfully"}
    # else status is embedded
    # Delete FileVectorMap
    vectors_map = db.query(models.FileVectorMap).filter(
        models.FileVectorMap.file_id == str(file.id),
        models.FileVectorMap.index_id == str(idx.id)
    ).first()

    # check and delele ids Pinecone
    if not vectors_map:
        raise HTTPException(status_code=404, detail="FileVectorMap not found for the specified file and index")
    vector_ids = vectors_map.vector_ids
    try:    
        result = delete_vectors_by_ids(idx.name, vector_ids)
        if result.get("status") != "deleted":
            raise HTTPException(status_code=500, detail="Failed to delete vectors from Pinecone")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vectors from Pinecone: {e}")
    # Delete FileVectorMap from DB
    db.delete(vectors_map)
    db.commit()
    # Delete file metadata from DB
    db.delete(file)
    db.commit()
    
    return {"detail": "File deleted successfully"}

