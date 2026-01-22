from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, List
import os
import logging

from services.admin_qa_service import AdminQAService

logger = logging.getLogger(__name__)

router = APIRouter()

# Get admin password from environment or use a default (not secure for production)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "k2admin2026")

# Singleton instance of AdminQAService
_admin_qa_service = None


def get_admin_qa_service() -> AdminQAService:
    """Get or create AdminQAService instance."""
    global _admin_qa_service
    if _admin_qa_service is None:
        _admin_qa_service = AdminQAService()
    return _admin_qa_service


def verify_admin_token(authorization: Optional[str] = Header(None)) -> bool:
    """
    Verify admin authentication token.
    
    Args:
        authorization: Authorization header (Bearer token)
        
    Returns:
        True if authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = parts[1]
    
    if token != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return True


# Request/Response Models
class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str


class QAPairRequest(BaseModel):
    question: str
    answer: str


class QAPairResponse(BaseModel):
    id: int
    question: str
    answer: str


class QAPairUpdateRequest(BaseModel):
    question: str
    answer: str


# Admin Routes
@router.post("/login", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    """
    Admin login endpoint.
    Returns a token (the password itself) for authentication.
    """
    if request.password == ADMIN_PASSWORD:
        return LoginResponse(
            success=True,
            token=ADMIN_PASSWORD,
            message="Login successful"
        )
    else:
        return LoginResponse(
            success=False,
            message="Invalid password"
        )


@router.get("/qa", response_model=List[QAPairResponse])
async def get_all_qa_pairs(authenticated: bool = Depends(verify_admin_token)):
    """
    Get all admin Q&A pairs.
    Requires authentication.
    """
    admin_qa_service = get_admin_qa_service()
    qa_pairs = admin_qa_service.get_all_qa_pairs()
    return qa_pairs


@router.get("/qa/{qa_id}", response_model=QAPairResponse)
async def get_qa_pair(qa_id: int, authenticated: bool = Depends(verify_admin_token)):
    """
    Get a specific Q&A pair by ID.
    Requires authentication.
    """
    admin_qa_service = get_admin_qa_service()
    qa_pair = admin_qa_service.get_qa_pair(qa_id)
    
    if not qa_pair:
        raise HTTPException(status_code=404, detail="Q&A pair not found")
    
    return qa_pair


@router.post("/qa", response_model=QAPairResponse)
async def create_qa_pair(
    request: QAPairRequest,
    authenticated: bool = Depends(verify_admin_token)
):
    """
    Create a new admin Q&A pair.
    Requires authentication.
    """
    if not request.question.strip() or not request.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer cannot be empty")
    
    admin_qa_service = get_admin_qa_service()
    new_pair = admin_qa_service.add_qa_pair(request.question, request.answer)
    
    logger.info(f"Created new admin Q&A pair: {new_pair['id']}")
    
    return new_pair


@router.put("/qa/{qa_id}", response_model=QAPairResponse)
async def update_qa_pair(
    qa_id: int,
    request: QAPairUpdateRequest,
    authenticated: bool = Depends(verify_admin_token)
):
    """
    Update an existing Q&A pair.
    Requires authentication.
    """
    if not request.question.strip() or not request.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer cannot be empty")
    
    admin_qa_service = get_admin_qa_service()
    updated_pair = admin_qa_service.update_qa_pair(qa_id, request.question, request.answer)
    
    if not updated_pair:
        raise HTTPException(status_code=404, detail="Q&A pair not found")
    
    logger.info(f"Updated admin Q&A pair: {qa_id}")
    
    return updated_pair


@router.delete("/qa/{qa_id}")
async def delete_qa_pair(
    qa_id: int,
    authenticated: bool = Depends(verify_admin_token)
):
    """
    Delete a Q&A pair.
    Requires authentication.
    """
    admin_qa_service = get_admin_qa_service()
    success = admin_qa_service.delete_qa_pair(qa_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Q&A pair not found")
    
    logger.info(f"Deleted admin Q&A pair: {qa_id}")
    
    return {"success": True, "message": "Q&A pair deleted successfully"}


@router.post("/qa/reload")
async def reload_qa_pairs(authenticated: bool = Depends(verify_admin_token)):
    """
    Reload Q&A pairs from file.
    Useful for manual file updates.
    Requires authentication.
    """
    admin_qa_service = get_admin_qa_service()
    admin_qa_service.reload()
    
    return {
        "success": True,
        "message": "Q&A pairs reloaded successfully",
        "count": len(admin_qa_service.get_all_qa_pairs())
    }
