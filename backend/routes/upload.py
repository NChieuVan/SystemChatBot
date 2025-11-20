from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from database import get_db
from minio_client import minio_client, MINIO_BUCKET
from services import vector_service
import models
from utils.security import get_current_user
from uuid import uuid4

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/")
async def upload_file(index_name: str = Form(...), file: UploadFile = Form(...), db: Session = Depends(get_db),current_user:models.User=Depends(get_current_user)):
    index_name  = index_name.strip()
    if not index_name:
        raise HTTPException(status_code=422, detail="Index name cannot be empty")
    if file is None or file.filename == "":
        raise HTTPException(status_code=422, detail="No file uploaded")
    
    # Verify index exists and belongs to user
    idx = db.query(models.VectorIndex).filter(
        models.VectorIndex.name == index_name,
        models.VectorIndex.user_id == current_user.id
    ).first()

    if not idx:
        raise HTTPException(status_code=404, detail="Index not found in your account")
    object_name = f"{idx.name}_{file.filename}"
    # upload stream to MinIO
    try:
        result = await run_in_threadpool(
            minio_client.put_object,
            MINIO_BUCKET,
            object_name,
            file.file,
            length=-1,
            content_type=file.content_type or "application/octet-stream",
            part_size=5 * 1024 * 1024,
            )
        if not result:
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file to storage: {str(e)}")
    # Caculate file size
    file.file.seek(0, 2)  # Move to end of file
    size_bytes = file.file.tell()
    file.file.seek(0)  # Reset to start of file
    # save metadata in DB
    meta = vector_service.add_file_metadata(db, index_id=idx.id, filename=file.filename, size_bytes=size_bytes)
    return {
        "file_id": str(meta.id),
        "filename": file.filename,
        "bucket": MINIO_BUCKET,
        "object": object_name,
        "size": size_bytes,
        "status": meta.status
    }
