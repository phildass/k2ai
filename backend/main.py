from fastapi import FastAPI
from backend.routes import chat

app = FastAPI()

# Mount the chat router at /api/chat
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])