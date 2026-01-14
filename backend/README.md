# K2 Communications Chatbot - Backend

FastAPI-based backend for the K2 Communications AI chatbot, powered by OpenAI GPT.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- OpenAI API key (Get one at https://platform.openai.com/api-keys)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**How to get your OpenAI API Key:**

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key immediately (you won't be able to see it again)
5. Paste it into your `.env` file

### 3. Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## API Endpoints

### Chat Endpoints

**POST /api/chat/** (Main endpoint)
- Send a message to the AI chatbot
- Note: Both `/api/chat` and `/api/chat/` work (the former redirects to the latter)
- Request body:
  ```json
  {
    "message": "Hello, I need help with PR services",
    "conversation_id": "optional-uuid",
    "language": "en",
    "context": {}
  }
  ```
- Response:
  ```json
  {
    "message": "AI response here",
    "conversation_id": "uuid",
    "suggestions": ["suggestion1", "suggestion2"],
    "metadata": {}
  }
  ```

**POST /api/chat/message** (Alternative endpoint for backward compatibility)
- Same functionality as POST /api/chat/

**GET /api/chat/conversation/{conversation_id}**
- Retrieve conversation history

### Service Endpoints

**GET /api/services/**
- Get all K2 Communications services

**GET /api/services/{service_id}**
- Get specific service details

### Feedback Endpoints

**POST /api/feedback/submit**
- Submit user feedback

**POST /api/feedback/lead**
- Capture lead information

## Configuration

The backend can be configured via environment variables in the `.env` file:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - OpenAI settings
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Optional - CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Optional - Environment
ENVIRONMENT=development
```

### Available Models

You can use different OpenAI models by changing the `LLM_MODEL` setting:
- `gpt-4-turbo-preview` (default, most capable)
- `gpt-4` (very capable, slightly older)
- `gpt-3.5-turbo` (faster, more cost-effective)

## Error Handling

The backend includes robust error handling:

- **Missing API Key**: If the `OPENAI_API_KEY` is not set or is set to the placeholder value, the chatbot will return a friendly error message directing users to configure the key.
- **API Errors**: Any OpenAI API errors are caught and return helpful fallback messages.
- **Network Issues**: Connection problems are handled gracefully with user-friendly messages.

## Development

### Project Structure

```
backend/
├── main.py              # Application entry point
├── routes/              # API route handlers
│   ├── chat.py         # Chat endpoints
│   ├── services.py     # Service information endpoints
│   └── feedback.py     # Feedback and lead capture
├── services/            # Business logic
│   └── chatbot_service.py  # OpenAI integration
├── models/              # Data models
│   └── schemas.py      # Pydantic models
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

### Running with Auto-reload

For development, use the `--reload` flag:

```bash
uvicorn main:app --reload --port 8000
```

This will automatically restart the server when you make code changes.

### Testing the API

You can test the API using:

1. **Interactive Docs**: Visit http://localhost:8000/docs
2. **curl**:
   ```bash
   curl -X POST http://localhost:8000/api/chat/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about your PR services"}'
   ```
3. **Python**:
   ```python
   import requests
   
   response = requests.post(
       "http://localhost:8000/api/chat/",
       json={"message": "Tell me about your PR services"}
   )
   print(response.json())
   ```

## Deployment

### Using Docker

Build and run with Docker:

```bash
docker build -t k2ai-backend .
docker run -p 8000:8000 --env-file .env k2ai-backend
```

### Production Considerations

1. **Environment**: Set `ENVIRONMENT=production` in `.env`
2. **CORS**: Configure `CORS_ORIGINS` with your frontend domain
3. **Secrets**: Use a proper secrets management system (not `.env` files)
4. **Database**: Replace in-memory conversation storage with a database
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Logging**: Configure proper logging and monitoring
7. **HTTPS**: Always use HTTPS in production

## Troubleshooting

### "API key not configured" error
- Make sure you've copied `.env.example` to `.env`
- Verify your OpenAI API key is correctly set in `.env`
- Don't use the placeholder value `your_openai_api_key_here`

### "Module not found" errors
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Consider using a virtual environment

### Port already in use
- Change the port: `uvicorn main:app --port 8001`
- Or kill the process using port 8000

### CORS errors from frontend
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Example: `CORS_ORIGINS=http://localhost:3000,https://yourdomain.com`

## Support

For issues or questions:
- Check the main project README: [../README.md](../README.md)
- Visit K2 Communications: https://www.k2communications.in/
- Review API documentation: http://localhost:8000/docs (when running)

## License

Proprietary - K2 Communications. All rights reserved.
