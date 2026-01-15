# CORS Fix Verification Guide

This document explains how to verify that the CORS fix for port 8081 is working correctly.

## Problem That Was Fixed

The frontend running on `http://localhost:8081` could not communicate with the backend because:
1. The CORS middleware was only allowing origins from ports 3000 and 8080
2. OPTIONS preflight requests from port 8081 were returning 400 Bad Request
3. POST requests to `/api/chat/` were failing with CORS errors

## What Was Changed

1. **backend/main.py**: Added `http://localhost:8081` and `http://127.0.0.1:8081` to the default CORS origins
2. **backend/.env.example**: Updated to document support for port 8081

## How to Verify the Fix

### Step 1: Start the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test the OPTIONS Preflight Request

In a new terminal, run:

```bash
curl -v -X OPTIONS http://localhost:8000/api/chat/ \
  -H "Origin: http://localhost:8081" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

**Expected Result:**
- Status: `200 OK` (not 400 Bad Request)
- Response headers should include:
  - `access-control-allow-origin: http://localhost:8081`
  - `access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`
  - `access-control-allow-credentials: true`
  - `access-control-allow-headers: Content-Type`

### Step 3: Test a POST Request

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Origin: http://localhost:8081" \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'
```

**Expected Result:**
- Status: `200 OK`
- JSON response with message and conversation_id

### Step 4: Test with Frontend

1. Start a simple HTTP server on port 8081:
   ```bash
   python3 -m http.server 8081
   ```

2. Open browser to: `http://localhost:8081/chat.html`

3. Type a message and click "Send"

**Expected Result:**
- No CORS errors in browser console
- Message sends successfully
- Bot response appears in the chat

## Troubleshooting

### Still Getting CORS Errors?

1. **Check which port your frontend is running on:**
   - Look at the URL in your browser
   - Common ports: 3000 (Next.js), 8080, 8081

2. **Verify the backend is using the updated code:**
   ```bash
   cd backend
   python -c "from main import app; import os; from dotenv import load_dotenv; load_dotenv(); default_origins='http://localhost:3000,http://localhost:8080,http://localhost:8081,http://127.0.0.1:3000,http://127.0.0.1:8080,http://127.0.0.1:8081'; origins=os.getenv('CORS_ORIGINS', default_origins).split(','); print('Allowed origins:', origins)"
   ```

3. **Create/update .env file if needed:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and ensure CORS_ORIGINS includes your port
   ```

4. **Restart the backend after any changes:**
   - Stop the server (Ctrl+C)
   - Start it again: `uvicorn main:app --reload --port 8000`

5. **Hard refresh your browser:**
   - Chrome/Firefox: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Clear cache if needed

### Using a Different Port?

If your frontend runs on a different port (e.g., 3001, 5000), add it to CORS_ORIGINS:

```bash
# In backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8081,http://localhost:3001
```

Then restart the backend.

## Summary

The fix is minimal and targeted:
- ✅ Port 8081 is now allowed in CORS configuration
- ✅ OPTIONS preflight requests work correctly
- ✅ POST requests to /api/chat/ work from port 8081
- ✅ Frontend on port 8081 can now communicate with backend

For more help, see `TROUBLESHOOTING.md`.
