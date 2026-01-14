from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.chatbot_service import ChatbotService
import uuid

router = APIRouter()

def get_chatbot_service():
    """Get or create chatbot service instance."""
    if not hasattr(get_chatbot_service, '_instance'):
        get_chatbot_service._instance = ChatbotService()
    return get_chatbot_service._instance

@router.post("/", response_model=ChatResponse)
@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI chatbot and get a response.
    Supports multilingual conversations and context-aware responses.
    
    This endpoint is available at both:
    - POST /api/chat (main endpoint)
    - POST /api/chat/message (alternative endpoint for backward compatibility)
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get chatbot service
        chatbot_service = get_chatbot_service()
        
        # Get chatbot response
        response = await chatbot_service.process_message(
            message=request.message,
            conversation_id=conversation_id,
            language=request.language,
            context=request.context
        )
        
        return ChatResponse(
            message=response["message"],
            conversation_id=conversation_id,
            suggestions=response.get("suggestions"),
            metadata=response.get("metadata")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Retrieve conversation history for a given conversation ID.
    """
    try:
        chatbot_service = get_chatbot_service()
        history = await chatbot_service.get_conversation_history(conversation_id)
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
