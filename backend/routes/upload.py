from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from minio_client import minio_client, MINIO_BUCKET
from services import vector_service
import models

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/")
async def upload_file(index_name: str = Form(...), file: UploadFile = None, db: Session = Depends(get_db)):
    idx = db.query(models.VectorIndex).filter(models.VectorIndex.name == index_name).first()
    if not idx:
        raise HTTPException(status_code=404, detail="Index not found")
    object_name = f"{file.filename}"
    # upload stream to MinIO
    minio_client.put_object(
        MINIO_BUCKET,
        object_name,
        file.file,
        length=-1,
        part_size=10*1024*1024,
        content_type=file.content_type or "application/octet-stream",
    )
    # save metadata in DB
    meta = vector_service.add_file_metadata(db, index_name=index_name, filename=file.filename, size_bytes=0)
    return {"file_id": str(meta.id), "filename": file.filename, "bucket": MINIO_BUCKET, "object": object_name}
