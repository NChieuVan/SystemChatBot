
from datetime import datetime
import uuid
from sqlalchemy.orm import Session,relationship
import models
from services import pinecone_service

from processing.preprocessing import Preprocessor
from services.pinecone_service import up_data_vectors
from services.file_vector_map_service import save_file_vector_map
from openAI import embedding_model

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

def get_index_by_name(db: Session, name: str, user_id: str):
    idx = db.query(models.VectorIndex).filter(models.VectorIndex.name == name,
                                             models.VectorIndex.user_id == user_id).first()
    try:
        if not idx:
            raise Exception("Index not found")
    except Exception as e:
        raise Exception(f"Lỗi khi lấy index: {str(e)}")
    return idx

def get_file_of_index(db: Session, index_id: str, file_name: str):
    file = db.query(models.IndexFile).filter(models.IndexFile.index_id == index_id,
                                            models.IndexFile.filename == file_name).first()
    try:
        if not file:
            raise Exception("File not found in the specified index")
    except Exception as e:
        raise Exception(f"Lỗi khi lấy file: {str(e)}")
    return file



def embedding_file(db: Session, index, file_obj):
    """
    - Lấy file từ MinIO
    - Preprocess (tách chunk)
    - Embedding
    - Upsert lên Pinecone
    - Lưu vector_ids vào FileVectorMap
    """
   
    # 1. Lấy file từ MinIO
    pre = Preprocessor()
    # print("embedding_file called:", index.name, file_obj.filename)
    docs = pre.load_pdf_from_minio(f"{index.name}_{file_obj.filename}")
    # print("Type of docs:", type(docs))
    # print("Docs value:", docs)
    if not docs:
        raise Exception("Không đọc được file từ MinIO hoặc file rỗng")
    split_docs = pre.split_documents(docs)
    if not split_docs:
        raise Exception("Không tách được nội dung file")
    # 2. Embedding (ví dụ: dùng OpenAIEmbeddings)
    try:
        model_embedding = embedding_model
    except Exception:
        model_embedding = None
    if not model_embedding:
        raise Exception("Không khởi tạo được model embedding")
    # 3. Upsert lên Pinecone
    result = up_data_vectors(index.name, split_docs, model_embedding)
    # 4. Lưu vector_ids vào FileVectorMap (giả sử result trả về ids)
    vector_ids = result.get("vector_ids", [])
    print("Vector IDs:", vector_ids)
    save_file_vector_map(db, str(file_obj.id), str(index.id), vector_ids)
    try:
        if not vector_ids:
            raise Exception("Không có vector_ids trả về từ Pinecone")
    except Exception as e:
        raise Exception(f"Lỗi khi lưu FileVectorMap: {str(e)}")
    # 5. Cập nhật trạng thái file
    file_obj.status = "embedded"
    db.commit()
    return result





