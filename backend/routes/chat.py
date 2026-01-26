from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
async def chat_endpoint(request: Request):
    # Example: simply echo back the user message
    try:
        data = await request.json()
        user_message = data.get("message", "")
        # You would replace the below with actual OpenAI/chat logic
        return {"reply": f"You said: {user_message}"}
    except Exception as e:
        return {"error": str(e)}