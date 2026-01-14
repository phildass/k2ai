# K2 Communications AI Chat - Integration Guide

## Quick Start

This guide provides complete instructions for running the K2 Communications AI chat system locally.

### Prerequisites
- Python 3.8+
- pip

### Step 1: Start the Backend (Port 8000)

```bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

### Step 2: Start the Frontend (Port 8080)

In a new terminal, from the repository root:

```bash
python3 -m http.server 8080
```

### Step 3: Open the Chat Interface

Navigate to: `http://localhost:8080/chat.html`

## API Testing with curl

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'
```

### Alternative Endpoint (Both Work)
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about crisis management"}'
```

## Configuration

### Environment Variables (backend/.env)

The backend automatically creates a `.env` file from `.env.example`. Key variables:

- `OPENAI_API_KEY`: Optional. If not set, uses predefined Q&A responses
- `CORS_ORIGINS`: Already configured for ports 8080 and 3000
- `LLM_MODEL`: GPT model to use (default: gpt-4-turbo-preview)

### Frontend Configuration (script.js)

The frontend is configured to send requests to:
```javascript
const API_URL = 'http://localhost:8000/api/chat/';
```

### CORS Configuration

The backend automatically allows requests from:
- `http://localhost:8080` (static HTML server)
- `http://127.0.0.1:8080` (static HTML server)
- `http://localhost:3000` (Next.js dev server)
- `http://127.0.0.1:3000` (Next.js dev server)

## Features

### Backend Features
✅ Dual endpoint support (`/api/chat/` and `/api/chat/message`)  
✅ Comprehensive request logging  
✅ CORS properly configured  
✅ FAQ/Q&A database fallback (works without API key)  
✅ Conversation history tracking  
✅ Multilingual support  
✅ Error handling and graceful fallbacks  

### Frontend Features
✅ Clean, modern chat interface  
✅ Real-time message updates  
✅ Loading indicators  
✅ Error handling with user feedback  
✅ Conversation persistence  
✅ Auto-scroll to latest message  

## Troubleshooting

### Backend Not Starting
- Check if port 8000 is already in use: `lsof -i :8000`
- Install dependencies: `pip install -r requirements.txt`

### Frontend Can't Connect to Backend
- Verify backend is running: `curl http://localhost:8000/health`
- Check browser console for CORS errors
- Ensure frontend is served from port 8080

### CORS Errors
- The backend is pre-configured for common development ports
- If using a different port, add it to `CORS_ORIGINS` in `backend/.env`

## Logging

The backend logs all incoming requests with:
- Request method and path
- Request headers
- Processing time
- Response status
- Chat message details

View logs in the terminal where the backend is running.

## Production Deployment

For production deployment:
1. Set `OPENAI_API_KEY` in environment variables
2. Update `CORS_ORIGINS` to include your production domain
3. Use a production WSGI server (e.g., Gunicorn)
4. Serve frontend through a web server (e.g., Nginx)
5. Enable HTTPS

## Support

For issues or questions, refer to the main README.md or create an issue in the repository.
