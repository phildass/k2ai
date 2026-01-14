# Development Guide

## Getting Started for Developers

This guide will help you set up your development environment and understand the codebase structure.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git
- VS Code or your preferred IDE
- OpenAI API key

## Initial Setup

### 1. Clone and Install

```bash
git clone https://github.com/phildass/k2ai.git
cd k2ai
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
```

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Code Structure

### Backend (FastAPI)

```
backend/
├── main.py                 # Application entry point
├── routes/                 # API endpoints
│   ├── chat.py            # Chat functionality
│   ├── services.py        # Service information
│   └── feedback.py        # Feedback and leads
├── services/              # Business logic
│   └── chatbot_service.py # LLM integration
├── models/                # Data models
│   └── schemas.py         # Pydantic models
└── utils/                 # Helper functions
```

### Frontend (Next.js)

```
frontend/src/
├── app/                   # Next.js App Router
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/            # React components
│   ├── ChatInterface.tsx # Chat UI
│   ├── ServiceList.tsx   # Services display
│   └── LeadForm.tsx      # Lead capture form
├── lib/                  # Utilities
│   └── api.ts           # API client
└── types/               # TypeScript types
    └── index.ts
```

## Key Concepts

### Chat Flow

1. User sends message via `ChatInterface` component
2. Frontend calls `/api/chat/message` endpoint
3. Backend `ChatbotService` processes message with OpenAI
4. Response returned with suggestions
5. Conversation history maintained in memory

### Adding a New Service

1. Edit `backend/routes/services.py`
2. Add service to `K2_SERVICES` array
3. Service automatically appears in API and UI

### Customizing AI Responses

Edit `backend/services/chatbot_service.py`:
- `get_system_prompt()` - Modify chatbot personality
- `_generate_suggestions()` - Customize follow-up options

## Development Workflow

### Making Changes

1. Create a feature branch
```bash
git checkout -b feature/your-feature
```

2. Make your changes

3. Test locally

4. Commit and push
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature
```

5. Create a Pull Request

### Hot Reloading

Both frontend and backend support hot reloading:
- **Frontend**: Changes to React components update automatically
- **Backend**: FastAPI reloads on file changes with `--reload` flag

## Testing

### Manual Testing

1. Test chat functionality
2. Verify all service endpoints
3. Test lead form submission
4. Check multilingual support

### API Testing

Use the interactive docs at http://localhost:8000/docs:
- Try different endpoints
- Test with various inputs
- Check response formats

## Common Issues

### Backend Won't Start
- Check if port 8000 is available
- Verify Python virtual environment is activated
- Ensure all dependencies are installed

### Frontend Build Errors
- Clear `.next` folder: `rm -rf .next`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)

### API Connection Errors
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Ensure `NEXT_PUBLIC_API_URL` is set correctly

## Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-...          # Required
LLM_MODEL=gpt-4-turbo-preview  # Optional
LLM_TEMPERATURE=0.7            # Optional
LLM_MAX_TOKENS=1000           # Optional
CORS_ORIGINS=http://localhost:3000  # Required
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Required
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Document functions with docstrings

### TypeScript/React
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks

## Debugging

### Backend
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frontend
```typescript
// Use console for debugging
console.log('Debug info:', data);
```

## Next Steps

1. Add database for conversation persistence
2. Implement user authentication
3. Add more chatbot flows
4. Integrate external services (calendar, email, etc.)
5. Add comprehensive testing

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
