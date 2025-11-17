from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

pc = Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index(index_name: str, dimension: int):
    """Create index if not exists + return status.
    - if created or exists: return {"status": "ready"}
    - if error: return {"status": "error", "error": str}
    """
    try:
        # Get list of all indexes
        existing = pc.list_indexes().names()

        # Create if not exists
        if index_name not in existing:
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV),
            )

        return {"status": "ready"}
    except Exception as e:
        print("Error creating Pinecone index:", e)
        return {"status": "error", "error": str(e)}
    
def delete_pinecone_index(index_name: str):
    """Delete Pinecone index by name."""
    try:
        pc.delete_index(name=index_name)
        return {"status": "deleted"}
    except Exception as e:
        print("Error deleting Pinecone index:", e)
        return {"status": "error", "error": str(e)}
