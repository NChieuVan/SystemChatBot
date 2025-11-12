from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import auth, chat, vector, upload

app = FastAPI(title="AI Chatbot Backend")

# Create tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(vector.router)
app.include_router(upload.router)

@app.get("/")
def root():
    return {"status": "Backend running"}
