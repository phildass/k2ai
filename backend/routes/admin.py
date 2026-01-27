import os
import logging
from typing import List, Optional

from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel

from backend.services.admin_qa_service import AdminQAService

logger = logging.getLogger(__name__)

router = APIRouter()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "k2admin2026")

_admin_qa_service = None

def get_admin_qa_service() -> AdminQAService:
    """Get or create AdminQAService instance."""
    global _admin_qa_service
    if _admin_qa_service is None:
        _admin_qa_service = AdminQAService()
    return _admin_qa_service

def verify_admin_token(authorization: Optional[str] = Header(None)) -> bool:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = parts[1]
    if token != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return True

# --- Models ---
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

# --- Routes ---

@router.post("/login", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    if request.password == ADMIN_PASSWORD:
        return LoginResponse(success=True, token=ADMIN_PASSWORD, message="Login successful")
    else:
        return LoginResponse(success=False, message="Invalid password")

@router.get("/qa", response_model=List[QAPairResponse])
async def get_all_qa_pairs(authenticated: bool = Depends(verify_admin_token)):
    admin_qa_service = get_admin_qa_service()
    qa_pairs = admin_qa_service.get_all_qa_pairs()
    return qa_pairs

@router.get("/qa/{qa_id}", response_model=QAPairResponse)
async def get_qa_pair(qa_id: int, authenticated: bool = Depends(verify_admin_token)):
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
    admin_qa_service = get_admin_qa_service()
    qa = admin_qa_service.add_qa_pair(request.question, request.answer)
    return qa

@router.put("/qa/{qa_id}", response_model=QAPairResponse)
async def update_qa_pair(
    qa_id: int,
    request: QAPairUpdateRequest,
    authenticated: bool = Depends(verify_admin_token)
):
    admin_qa_service = get_admin_qa_service()
    qa = admin_qa_service.update_qa_pair(qa_id, request.question, request.answer)
    if not qa:
        raise HTTPException(status_code=404, detail="Q&A pair not found")
    return qa

@router.delete("/qa/{qa_id}")
async def delete_qa_pair(
    qa_id: int,
    authenticated: bool = Depends(verify_admin_token)
):
    admin_qa_service = get_admin_qa_service()
    success = admin_qa_service.delete_qa_pair(qa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Q&A pair not found")
    return {"success": True, "id": qa_id}