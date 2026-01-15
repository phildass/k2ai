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

# Check OpenAI API configuration at startup
PLACEHOLDER_API_KEY = "your_openai_api_key_here"
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == PLACEHOLDER_API_KEY:
    logger.warning("="*70)
    logger.warning("⚠ OPENAI_API_KEY is not configured!")
    logger.warning("The chatbot will use predefined Q&A only.")
    logger.warning("For live AI responses, please:")
    logger.warning("1. Create backend/.env file (copy from .env.example)")
    logger.warning("2. Set OPENAI_API_KEY=your-actual-key")
    logger.warning("3. Restart the server")
    logger.warning("See OPENAI_SETUP_GUIDE.md for detailed instructions")
    logger.warning("="*70)
else:
    logger.info("="*70)
    logger.info("✓ OpenAI API key loaded successfully")
    logger.info(f"✓ Using model: {os.getenv('LLM_MODEL', 'gpt-4-turbo-preview')}")
    logger.info("✓ Live AI assistant is enabled")
    logger.info("="*70)

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
    """
    Health check endpoint that includes OpenAI API status.
    Returns detailed health information about the service.
    """
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "api": {
            "openai_configured": False,
            "openai_key_status": "missing",
            "llm_model": os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
        },
        "features": {
            "predefined_qa": True,
            "live_ai": False
        }
    }
    
    # Check OpenAI API key status
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != PLACEHOLDER_API_KEY:
        health_status["api"]["openai_configured"] = True
        health_status["api"]["openai_key_status"] = "configured"
        health_status["features"]["live_ai"] = True
    elif api_key == PLACEHOLDER_API_KEY:
        health_status["api"]["openai_key_status"] = "placeholder"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)