from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
USE_SSL = os.getenv("MINIO_USE_SSL", "false").lower() == "true"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=USE_SSL
)

if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)