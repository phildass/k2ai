#!/bin/bash
# Simple test script for K2 AI server

echo "========================================="
echo "K2 AI Server Test Script"
echo "========================================="
echo ""

# Start server in background
echo "Starting server..."
node index.js > /tmp/k2ai_server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
sleep 2

# Test root endpoint
echo ""
echo "Testing root endpoint (/)..."
RESPONSE=$(curl -s http://localhost:3000/)
if [ "$RESPONSE" == "Testing page for K2 AI" ]; then
    echo "✓ PASS: Root endpoint returns correct message"
else
    echo "✗ FAIL: Expected 'Testing page for K2 AI', got '$RESPONSE'"
fi

# Test health endpoint
echo ""
echo "Testing health endpoint (/health)..."
HEALTH=$(curl -s http://localhost:3000/health)
if echo "$HEALTH" | grep -q '"status":"healthy"'; then
    echo "✓ PASS: Health endpoint returns healthy status"
else
    echo "✗ FAIL: Health endpoint did not return expected status"
fi

# Show server logs
echo ""
echo "Server logs:"
cat /tmp/k2ai_server.log

# Cleanup
echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
echo "Done!"
