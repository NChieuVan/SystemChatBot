from sqlalchemy.orm import Session
from models import FileVectorMap

def save_file_vector_map(db: Session, file_id, index_id, vector_ids: list):
    mapping = db.query(FileVectorMap).filter_by(file_id=file_id, index_id=index_id).first()
    if mapping:
        mapping.vector_ids = vector_ids
        db.commit()
        db.refresh(mapping)
    else:
        mapping = FileVectorMap(file_id=file_id, index_id=index_id, vector_ids=vector_ids)
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
    return mapping

def get_vector_ids_by_file(db: Session, file_id, index_id):
    mapping = db.query(FileVectorMap).filter_by(file_id=file_id, index_id=index_id).first()
    return mapping.vector_ids if mapping else []

def delete_file_vector_map(db: Session, file_id, index_id):
    mapping = db.query(FileVectorMap).filter_by(file_id=file_id, index_id=index_id).first()
    if mapping:
        db.delete(mapping)
        db.commit()
