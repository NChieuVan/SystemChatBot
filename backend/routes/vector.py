from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import vector_service
import schema
from utils.security import get_current_user

router = APIRouter(prefix="/api/indexes", tags=["Vector"])

@router.get("/", response_model=list[schema.IndexOut])
def list_indexes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return vector_service.get_indexes(db, user_id=str(current_user.id))

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
def delete_index(name: str, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    if not name or not name.strip():
        raise HTTPException(status_code=422, detail="Tên index không được để trống.")
    result = vector_service.delete_index(db, name, user_id=str(current_user.id))
    if not result:
        raise HTTPException(status_code=404, detail="Index not found")
    return {"message": "Index deleted"}

# recive file and status
@router.post("/{index_name}/{file_name}")
def embedding_file(index_name: str, file_name: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not index_name or not index_name.strip():
        raise HTTPException(status_code=422, detail="Tên index không được để trống.")
    index = vector_service.get_index_by_name(db, index_name.strip(), user_id=str(current_user.id))
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")
    file_obj = vector_service.get_file_of_index(db, index_id=str(index.id), file_name=file_name)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found in the specified index")
    print("---- Embedding file: "+str(file_obj.filename)+" ----" +str(file_obj.status)+" ----")
    if file_obj.status == "embedded":
        return {"file_name": file_name, "status": "embedded", "message": "File đã được nhúng!"}
    
    # Thực hiện embedding (preprocess, embedding, upsert Pinecone)
    try:
        result = vector_service.embedding_file(db, index, file_obj)
        # Sau khi embedding thành công, cập nhật trạng thái file
        file_obj.status = "embedded"
        db.commit()
        return {"file_name": file_name, "status": "embedded", "message": "Nhúng dữ liệu thành công!", "detail": result}
    except Exception as e:
        return {"file_name": file_name, "status": "error", "message": str(e)}