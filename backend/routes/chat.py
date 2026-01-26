from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        # IMPORTANT: Try "answer" and/or "response" as the key
        return {"answer": f"You said: {user_message}"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}