from fastapi import FastAPI
from backend.routes import chat, admin  # <--- Make sure both are imported

app = FastAPI()

# Set up chatbot endpoint
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# Set up admin endpoint
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])