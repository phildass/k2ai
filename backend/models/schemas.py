from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = None
    language: str = Field(default="en", description="Language code (en, hi, ta, etc.)")
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    suggestions: Optional[List[str]] = None
    metadata: Optional[dict] = None
    answer_source: Optional[str] = Field(default="ai", description="Source of answer: 'faq_match' or 'ai'")

class LeadCaptureRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    service_interest: str
    message: Optional[str] = None

class FeedbackRequest(BaseModel):
    conversation_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    sentiment: Optional[str] = None

class ServiceInfo(BaseModel):
    id: str
    name: str
    description: str
    key_features: List[str]
    use_cases: List[str]
