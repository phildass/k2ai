#!/bin/bash

echo "🚀 Starting K2 AI Application..."

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Setting up Python environment..."
    python3 -m venv venv
    venv/bin/pip install -r backend/requirements.txt
fi

# Start Python FastAPI backend in background
echo "📦 Starting Python backend on port 8000..."
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
PYTHON_PID=$!
cd ..

# Wait for Python backend to be ready
echo "⏳ Waiting for Python backend to start..."
sleep 5

# Start Node.js frontend on PORT from Render
echo "🌐 Starting Node.js frontend on port ${PORT:-10000}..."
PYTHON_BACKEND_URL=http://localhost:8000 node index.js &
NODE_PID=$!

echo "✅ Application started!"
echo "   - Python Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:${PORT:-10000}"

# Wait for any process to exit
wait -n

# Kill all background processes
kill $PYTHON_PID $NODE_PID 2>/dev/null
