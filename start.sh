#!/bin/bash

echo "🚀 Starting K2 AI Application..."

# Start Python FastAPI backend in background
echo "📦 Starting Python backend on port 8000..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
PYTHON_PID=$!
cd ..

# Wait for Python backend to be ready
echo "⏳ Waiting for Python backend to start..."
sleep 5

# Start Node.js frontend
echo "🌐 Starting Node.js frontend on port 3000..."
PYTHON_BACKEND_URL=http://localhost:8000 node server.js &
NODE_PID=$!

echo "✅ Application started!"
echo "   - Python Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - Admin Panel: http://localhost:3000/admin.html"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for any process to exit
wait -n

# Kill all background processes
kill $PYTHON_PID $NODE_PID 2>/dev/null
