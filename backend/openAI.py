import os
from dotenv import load_dotenv
# import OPENAI Embeddings
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)