import uuid
from datetime import datetime

def gen_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.utcnow()
