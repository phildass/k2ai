from fastapi import FastAPI
from backend.routes import chat, admin

app = FastAPI()

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])