# Quick Start Guide

Get the K2 AI Chatbot running in 5 minutes!

## Option 1: Docker Compose (Easiest)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/phildass/k2ai.git
cd k2ai
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. **Start the application**
```bash
docker-compose up --build
```

4. **Open your browser**
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs

That's it! The chatbot is now running.

## Option 2: Manual Setup (For Development)

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- OpenAI API key

### Backend Setup (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the backend
uvicorn main:app --reload --port 8000
```

Backend will be available at http://localhost:8000

### Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Default values should work for local development

# Run the frontend
npm run dev
```

Frontend will be available at http://localhost:3000

## Testing the Application

### 1. Test the Backend API

Visit http://localhost:8000/docs to see the interactive API documentation.

Try the `/api/chat/message` endpoint:
```json
{
  "message": "Tell me about your PR services",
  "language": "en"
}
```

### 2. Test the Frontend

1. Open http://localhost:3000
2. You should see the K2 Communications chatbot interface
3. Try asking: "What services do you offer?"
4. Click on "Get in Touch" to test the lead form
5. View the services in the sidebar

### 3. Test Multilingual Support

Try sending a message in Hindi:
```json
{
  "message": "मुझे आपकी सेवाओं के बारे में बताएं",
  "language": "hi"
}
```

## Common Issues

### Backend Issues

**Port 8000 already in use**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
# Or use a different port
uvicorn main:app --reload --port 8001
```

**OpenAI API Error**
- Verify your API key is correct in `backend/.env`
- Check your OpenAI account has credits
- Ensure the API key has the correct permissions

**Import Errors**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port 3000 already in use**
```bash
# Kill the process
lsof -ti:3000 | xargs kill -9
# Or Next.js will automatically use port 3001
```

**Build Errors**
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

**API Connection Error**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

### Docker Issues

**Containers won't start**
```bash
# Stop all containers
docker-compose down

# Remove old containers and rebuild
docker-compose up --build --force-recreate
```

**Backend container fails**
- Check logs: `docker-compose logs backend`
- Verify `.env` file exists in `backend/` directory
- Ensure OpenAI API key is set

## Next Steps

### Customize the Chatbot

1. **Modify the AI personality**
   - Edit `backend/services/chatbot_service.py`
   - Update the `get_system_prompt()` method

2. **Add/modify services**
   - Edit `backend/routes/services.py`
   - Update the `K2_SERVICES` array

3. **Customize the UI**
   - Edit components in `frontend/src/components/`
   - Update styling in `frontend/tailwind.config.js`

### Add Database (Optional)

Replace in-memory storage with a database:
1. Choose a database (PostgreSQL, MongoDB, etc.)
2. Add database connection in `backend/`
3. Update `ChatbotService` to use database instead of `self.conversations`

### Deploy to Production

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

Quick deployment options:
- **Frontend**: Deploy to Vercel with one click
- **Backend**: Deploy to Railway or Render
- **Full Stack**: Use Docker on any cloud provider

## Useful Commands

### Backend
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run on different port
uvicorn main:app --port 8001

# Check Python version
python --version

# List installed packages
pip list
```

### Frontend
```bash
# Development mode
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Check for updates
npm outdated
```

### Docker
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Remove all data
docker-compose down -v
```

## Getting Help

- **Documentation**: Check the `docs/` folder
- **API Reference**: `docs/API.md`
- **Development Guide**: `docs/DEVELOPMENT.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **Chatbot Flows**: `docs/CHATBOT_FLOWS.md`

## Development Workflow

1. Make changes to code
2. Changes auto-reload in development mode
3. Test locally
4. Commit and push to GitHub
5. Deploy to production

Enjoy building with K2 AI Chatbot! 🚀
