from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
import time

from routes import chat, services, feedback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="K2 Communications AI Chatbot API",
    description="AI-powered chatbot for K2 Communications - India's premier PR agency",
    version="1.0.0"
)

# CORS configuration
# Default to common development origins if not specified in environment
default_origins = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080"
origins = os.getenv("CORS_ORIGINS", default_origins).split(",")

# For development, you can use ["*"] as origins to allow all. It's less secure!
if not origins or origins == [""]:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    # Log only non-sensitive headers
    safe_headers = {
        k: v for k, v in request.headers.items() 
        if k.lower() not in ['authorization', 'cookie', 'x-api-key']
    }
    logger.info(f"Request headers (filtered): {safe_headers}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Completed {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}s")
    
    return response

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(services.router, prefix="/api/services", tags=["services"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])

@app.get("/")
async def root():
    return {
        "message": "K2 Communications AI Chatbot API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)