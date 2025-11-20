from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from minio_client import minio_client, MINIO_BUCKET
from io import BytesIO
import tempfile
class Preprocessor:
    def __init__(self,chunk_size:int=1000,chunk_overlap:int=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_pdf_from_directory(self,directory_path:str="../data") -> List[Document]:
        """Load all files from a directory and return as list of Documents."""
        loader = DirectoryLoader(directory_path, glob="**/*.*", loader_cls=PyPDFLoader)
        documents = loader.load()
        return documents
    
    def load_pdf_from_minio(self, object_name: str) -> List[Document]:
        """Load PDF directly from MinIO as Documents."""
        
        print(f"[Preprocessor] Loading from MinIO: bucket={MINIO_BUCKET}, object={object_name}")
        try:
            response = minio_client.get_object(MINIO_BUCKET, object_name)
            pdf_bytes = response.read()
            print(f"[Preprocessor] Bytes loaded: {len(pdf_bytes)}")
            # Lưu ra file tạm
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_path = tmp_file.name
            loader = PyPDFLoader(file_path=tmp_path)
            documents = loader.load()
            print(f"[Preprocessor] Documents loaded: {len(documents)}")
            return documents
        except Exception as e:
            print(f"[Preprocessor] Error loading PDF from MinIO: {e}")
            return []
    
    def filler_short_documents(self,docuemnts:List[Document]) -> List[Document]:
        """Fill short documents to meet the minimum length requirement."""
        filled_documents:List[Document] = []
        for doc in docuemnts:
            filled_documents.append(
                Document(
                    page_content=doc.page_content,
                    metadata={
                        "source": doc.metadata.get("source",""),
                        "page": doc.metadata.get("page","")
                    }
                )
            )
        return filled_documents
    
    def split_documents(self,documents:List[Document]) -> List[Document]:
        """
        Splits the content of each Document in the input list into smaller chunks.
        
        Args:
            documents (List[Document]): List of Document objects to be split.
            chunk_size (int): The maximum size of each chunk.
            chunk_overlap (int): The number of overlapping characters between chunks.
            
        Returns:
            List[Document]: A new list of Document objects with split content.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        split_docs = text_splitter.split_documents(documents=documents)
        return split_docs
    

    
if __name__ == "__main__":
    preprocessor = Preprocessor()
    docs = preprocessor.load_pdf_from_minio("chatbot-data/van_NguyenChieuVan_AI_Engineer.pdf")
    split_docs = preprocessor.split_documents(docs)

    
    


