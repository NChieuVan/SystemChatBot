import os
from dotenv import load_dotenv
# import OPENAI Embeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o", temperature=0)