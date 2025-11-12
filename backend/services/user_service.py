from sqlalchemy.orm import Session
import models
from utils.security import hash_password, verify_password

def create_user(db: Session, email: str, password: str, name: str | None = None):
    if db.query(models.User).filter(models.User.email == email).first():
        return None
    u = models.User(email=email, password_hash=hash_password(password), name=name)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def authenticate(db: Session, email: str, password: str):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    if not verify_password(password, u.password_hash):
        return None
    return u
