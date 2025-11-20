from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from typing import List
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
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
# Updata to Pinecone API
def up_data_vectors(index_name: str, documents:List[Document], model_embedding) -> dict:
    """
    - Args:
        index_name (str): Name of the Pinecone index.
        docments (List[Document]): List of Document objects to be upserted.
        model_embedding: Embedding model with an 'embed_documents' method. ex: OpenAIEmbeddings(), HuggingFaceEmbeddings()
    - Returns:
        dict: Status of the upsert operation."""
    try:
        document_search = PineconeVectorStore.from_documents(
            documents=documents,
            embedding=model_embedding,
            index_name=index_name,
        )
        # Lấy danh sách vector_ids vừa upsert
    
        vector_ids = []
        if hasattr(document_search, 'added_ids'):
            vector_ids = document_search.added_ids
        elif hasattr(document_search, 'ids'):
            vector_ids = document_search.ids
        # Trả về status và vector_ids
        return {"status": "upserted", "vector_ids": vector_ids}
    except Exception as e:
        print("Error upserting vectors to Pinecone index:", e)
        return {"status": "error", "error": str(e), "vector_ids": []}

#Load data from Pinecone index
def load_vectors(index_name: str, model_embedding) -> PineconeVectorStore:
    """
    - Args:
        index_name (str): Name of the Pinecone index.
        model_embedding: Embedding model with an 'embed_documents' method. ex: OpenAIEmbeddings(), HuggingFaceEmbeddings()
    - Returns:
        PineconeVectorStore: The loaded Pinecone vector store."""
    try:
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=model_embedding,
        )
        return vector_store
    except Exception as e:
        print("Error loading vectors from Pinecone index:", e)
        raise Exception(str(e))
    
def retrieve_documents(index_name: str, model_embedding, top_k: int = 5) -> List[Document]:
    """
    - Args:
        index_name (str): Name of the Pinecone index.
        model_embedding: Embedding model with an 'embed_documents' method. ex: OpenAIEmbeddings(), HuggingFaceEmbeddings()
        top_k (int): Number of top similar documents to retrieve.
    """
    try:
        vector_store = load_vectors(index_name, model_embedding)
        similar_docs = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k})
        return similar_docs
    except Exception as e:
        print("Error retrieving similar documents from Pinecone index:", e)
        raise Exception(str(e))
    
def add_more_documents(index_name: str, documents: List[Document], model_embedding) -> dict:
    """
    - Args:
        index_name (str): Name of the Pinecone index.
        documents (List[Document]): List of Document objects to be added.
        model_embedding: Embedding model with an 'embed_documents' method. ex: OpenAIEmbeddings(), HuggingFaceEmbeddings()
    - Returns:
        dict: Status of the add operation."""
    try:
        vector_store = load_vectors(index_name, model_embedding)
        vector_store.add_documents(documents)
        return {"status": "added"}
    except Exception as e:
        print("Error adding documents to Pinecone index:", e)
        return {"status": "error", "error": str(e)}

def delete_documents(index_name: str, ids: List[str], model_embedding) -> dict:
    """
    - Args:
        index_name (str): Name of the Pinecone index.
        ids (List[str]): List of document IDs to be deleted.
        model_embedding: Embedding model with an 'embed_documents' method. ex: OpenAIEmbeddings(), HuggingFaceEmbeddings()
    - Returns:
        dict: Status of the delete operation."""
    try:
        vector_store = load_vectors(index_name, model_embedding)
        vector_store.delete(ids)
        return {"status": "deleted"}
    except Exception as e:
        print("Error deleting documents from Pinecone index:", e)
        return {"status": "error", "error": str(e)}