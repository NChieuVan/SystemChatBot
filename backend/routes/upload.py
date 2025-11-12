from fastapi import APIRouter, File, UploadFile, HTTPException
from ..minio_client import minio_client, MINIO_BUCKET_NAME,MINIO_ENDPOINT
import uuid

router = APIRouter(prefix="/api/upload", tags=["Upload"])
@router.post("/")
async def upload_file(file:UploadFile)-> str:
    try:
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}_{file.filename}" # Unique file name to avoid collisions. Ex: file:book.pdf -> 123e4567-e89b-12d3-a456-426614174000_book.pdf

        # Upload the file to MinIO
        result = minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=file_name,
            data=file.file,
            length=-1,
            part_size=10*1024*1024,  # 10MB part size
            content_type=file.content_type
        )

        # Return the file URL or identifier
        url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET_NAME}/{file_name}"
        return {"file_id": file_id,"file_name":file_name,"file_url": url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")