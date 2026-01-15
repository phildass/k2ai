# K2AI Chatbot - Troubleshooting & Verification Guide

## Quick Diagnostics

Run these commands to quickly check your setup:

```bash
# Check if backend is running
curl http://localhost:8000/health

# Test with predefined Q&A (should always work)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'

# Test with unique question (requires OpenAI API)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the future of AI in public relations?"}'

# Run comprehensive test
cd backend
python test_openai_connection.py
```

## Common Issues and Solutions

### 1. "OpenAI API key is missing" Error

**Symptoms:**
- Chat responses say "chatbot is not fully configured"
- Health check shows `"openai_configured": false`
- Backend logs show warning about missing API key

**Root Causes:**
- `.env` file doesn't exist in `backend/` directory
- `OPENAI_API_KEY` not set in `.env` file
- API key is still set to placeholder `your_openai_api_key_here`

**Solutions:**

```bash
# Step 1: Check if .env exists
ls -la backend/.env

# Step 2: If not, create from example
cd backend
cp .env.example .env

# Step 3: Edit and add your API key
nano .env
# Change: OPENAI_API_KEY=your_openai_api_key_here
# To:     OPENAI_API_KEY=sk-proj-your-actual-key

# Step 4: Restart backend
# Kill existing process and restart
uvicorn main:app --reload --port 8000
```

**Verification:**
```bash
# Check health endpoint
curl http://localhost:8000/health | python -m json.tool

# Should show:
# "openai_configured": true,
# "openai_key_status": "configured",
# "live_ai": true
```

---

### 2. Invalid or Expired API Key

**Symptoms:**
- Error: "Incorrect API key provided"
- Error: "401 Unauthorized"
- Backend logs show authentication errors

**Solutions:**

1. **Verify API key on OpenAI platform:**
   ```bash
   # Visit https://platform.openai.com/api-keys
   # Check if your key is still active
   ```

2. **Generate new API key:**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the new key (you won't see it again!)
   - Update `backend/.env` with new key

3. **Check for extra spaces or characters:**
   ```bash
   # Make sure no spaces before/after the key
   # Correct:   OPENAI_API_KEY=sk-proj-abc123
   # Incorrect: OPENAI_API_KEY= sk-proj-abc123
   # Incorrect: OPENAI_API_KEY=sk-proj-abc123 
   ```

**Test your API key directly:**
```bash
cd backend
python test_openai_connection.py
```

---

### 3. Rate Limit or Quota Exceeded

**Symptoms:**
- Error: "Rate limit exceeded"
- Error: "You exceeded your current quota"
- Intermittent failures

**Solutions:**

1. **Check your usage and limits:**
   - Visit https://platform.openai.com/usage
   - View current usage and remaining quota

2. **Add credits to your account:**
   - Visit https://platform.openai.com/account/billing
   - Add payment method and credits

3. **Set usage limits:**
   - Visit https://platform.openai.com/account/limits
   - Set monthly spending cap
   - Set up usage alerts

4. **Switch to cheaper model (temporary fix):**
   ```env
   # In backend/.env
   LLM_MODEL=gpt-3.5-turbo  # Cheaper than gpt-4
   ```

5. **Implement request throttling:**
   - Add delays between requests
   - Use caching for common questions
   - Rely more on predefined Q&A

---

### 4. Backend Won't Start

**Symptoms:**
- `uvicorn` command fails
- Import errors
- Module not found errors

**Solutions:**

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Check Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

3. **Use virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

4. **Check for port conflicts:**
   ```bash
   # Check if port 8000 is already in use
   lsof -i :8000  # On Linux/Mac
   netstat -ano | findstr :8000  # On Windows
   
   # If in use, kill the process or use different port
   uvicorn main:app --reload --port 8001
   ```

---

### 5. CORS Errors (Frontend Can't Connect)

**Symptoms:**
- Browser console shows CORS errors
- Frontend can't reach backend
- "Access-Control-Allow-Origin" errors

**Solutions:**

1. **Check CORS configuration:**
   ```env
   # In backend/.env
   CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8081,https://your-domain.com
   ```

2. **Verify frontend URL matches:**
   ```bash
   # If frontend is on port 3001, add it:
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8080,http://localhost:8081
   # Common ports: 3000 (Next.js), 8080 (simple server), 8081 (alternative simple server)
   ```

3. **For development, temporarily allow all origins:**
   ```env
   # backend/.env (DEVELOPMENT ONLY - NOT FOR PRODUCTION!)
   CORS_ORIGINS=*
   ```

4. **Check backend logs for CORS warnings**

---

### 6. Slow or No Responses

**Symptoms:**
- Requests timeout
- Very slow responses (>30 seconds)
- Intermittent failures

**Solutions:**

1. **Check OpenAI status:**
   - Visit https://status.openai.com/
   - Check for ongoing incidents

2. **Use faster model:**
   ```env
   # In backend/.env
   LLM_MODEL=gpt-3.5-turbo  # Much faster than gpt-4
   ```

3. **Reduce token limits:**
   ```env
   # In backend/.env
   LLM_MAX_TOKENS=500  # Shorter responses = faster
   ```

4. **Check network connectivity:**
   ```bash
   # Test connection to OpenAI
   curl -I https://api.openai.com
   
   # Check DNS resolution
   nslookup api.openai.com
   ```

5. **Check firewall/proxy settings:**
   - Ensure outbound HTTPS is allowed
   - Whitelist `api.openai.com` if needed

---

### 7. All Responses are Predefined (No Live AI)

**Symptoms:**
- Every response shows `"source": "predefined"`
- Never get `"source": "llm"` responses
- Works but not using OpenAI

**Solutions:**

1. **Ask unique questions:**
   ```bash
   # This will match predefined Q&A:
   "What services do you offer?"
   
   # This should trigger OpenAI:
   "What are the emerging trends in PR for 2026?"
   ```

2. **Check API key is configured:**
   ```bash
   curl http://localhost:8000/health
   # Should show "live_ai": true
   ```

3. **Check backend logs:**
   ```bash
   # Look for:
   # "Calling OpenAI API..."
   # or
   # "OpenAI API key not configured"
   ```

4. **Verify environment variables loaded:**
   ```bash
   cd backend
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY', 'NOT SET')[:20])"
   ```

---

### 8. Frontend UI Issues

**Symptoms:**
- Chat interface doesn't load
- Messages don't send
- No response from server

**Solutions:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check frontend configuration:**
   ```javascript
   // In script.js or frontend config
   const API_URL = 'http://localhost:8000/api/chat/';
   // Make sure this matches your backend URL
   ```

3. **Check browser console for errors:**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

4. **Serve frontend properly:**
   ```bash
   # For simple HTML version
   python -m http.server 8080
   # Then open http://localhost:8080/chat.html
   
   # For Next.js version
   cd frontend
   npm install
   npm run dev
   # Then open http://localhost:3000
   ```

---

### 9. Database/Conversation History Issues

**Symptoms:**
- Conversation context is lost
- "Conversation not found" errors

**Note:** Current version uses in-memory storage.

**Solutions:**

1. **Restart backend** (clears all conversation history)

2. **For production, implement persistent storage:**
   - Add database (PostgreSQL, MongoDB)
   - Configure DATABASE_URL in .env
   - Implement conversation persistence

---

### 10. Environment Variables Not Loading

**Symptoms:**
- Settings from `.env` file not applied
- Always using default values

**Solutions:**

1. **Check .env file location:**
   ```bash
   # Must be in backend/ directory
   ls -la backend/.env
   ```

2. **Check .env file format:**
   ```env
   # Correct format:
   OPENAI_API_KEY=sk-proj-abc123
   LLM_MODEL=gpt-4-turbo-preview
   
   # Incorrect (no spaces around =):
   OPENAI_API_KEY = sk-proj-abc123
   
   # Incorrect (no quotes needed):
   OPENAI_API_KEY="sk-proj-abc123"
   ```

3. **Restart backend after changing .env:**
   ```bash
   # .env is only loaded at startup
   # Must restart for changes to take effect
   ```

4. **Test environment loading:**
   ```bash
   cd backend
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', os.getenv('OPENAI_API_KEY', 'NOT SET')[:20])"
   ```

---

## Diagnostic Commands

### Check System Status

```bash
# Full health check
curl http://localhost:8000/health | python -m json.tool

# Check API documentation
curl http://localhost:8000/docs  # Or open in browser

# View backend logs
# (Look at terminal where uvicorn is running)
```

### Test Specific Features

```bash
# Test predefined Q&A
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}' | python -m json.tool

# Test live AI (requires API key)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing in simple terms"}' | python -m json.tool

# Test with conversation ID
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_id": "test-123"}' | python -m json.tool
```

### Run Comprehensive Test

```bash
cd backend
python test_openai_connection.py
```

Expected output:
```
==============================================================
OpenAI API Connection Test
==============================================================

✓ .env file found
✓ OpenAI API key is configured
ℹ Key prefix: sk-proj-abc123...
ℹ Testing connection with model: gpt-4-turbo-preview
ℹ Sending test message to OpenAI...
✓ Successfully connected to OpenAI API!
✓ Model: gpt-4-turbo-preview
✓ Live AI assistant is working!

------------------------------------------------------------
Test Response:
------------------------------------------------------------
Hello, I am working!
------------------------------------------------------------

==============================================================
ALL TESTS PASSED!
==============================================================

✓ Your OpenAI integration is working correctly!
✓ The K2AI chatbot can now provide live AI responses.
```

---

## Log Analysis

### What to Look For in Logs

**Good Startup Logs:**
```
✓ OpenAI API key loaded successfully
✓ Using model: gpt-4-turbo-preview
✓ Live AI assistant is enabled
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Warning Signs:**
```
⚠ OPENAI_API_KEY is not configured!
The chatbot will use predefined Q&A only.
```

**Error Signs:**
```
ERROR: Failed to connect to OpenAI API
Error: Incorrect API key provided
```

### Enable Debug Logging

```bash
# Start with debug logging
LOG_LEVEL=DEBUG uvicorn main:app --reload --port 8000
```

---

## Getting Help

If none of these solutions work:

1. **Check the logs thoroughly:**
   - Backend console output
   - Browser console (F12)
   - Network requests in browser DevTools

2. **Run the test script:**
   ```bash
   cd backend
   python test_openai_connection.py
   ```

3. **Verify your setup:**
   - Python version (3.8+)
   - All dependencies installed
   - .env file exists and formatted correctly
   - API key is valid and has credits

4. **Consult documentation:**
   - `OPENAI_SETUP_GUIDE.md` - Setup instructions
   - `README.md` - General overview
   - `backend/QA_IMPLEMENTATION.md` - Q&A system details

5. **Check external services:**
   - OpenAI status: https://status.openai.com/
   - OpenAI API docs: https://platform.openai.com/docs

6. **Create minimal test case:**
   ```bash
   # Test OpenAI directly
   cd backend
   python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print(client.chat.completions.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hi'}]).choices[0].message.content)"
   ```

---

## Prevention Tips

1. **Use version control wisely:**
   - Never commit `.env` files
   - Use `.env.example` as template
   - Document required variables

2. **Set up monitoring:**
   - Monitor OpenAI usage
   - Set spending limits
   - Configure alerts

3. **Regular testing:**
   - Run `test_openai_connection.py` regularly
   - Test both predefined and AI responses
   - Check logs for errors

4. **Keep dependencies updated:**
   ```bash
   cd backend
   pip install --upgrade -r requirements.txt
   ```

5. **Backup configuration:**
   - Keep separate dev/staging/prod keys
   - Document your setup
   - Use secrets management in production

---

## Quick Reference Card

```bash
# START BACKEND
cd backend
uvicorn main:app --reload --port 8000

# TEST CONNECTION
python test_openai_connection.py

# CHECK HEALTH
curl http://localhost:8000/health

# TEST CHAT
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# VIEW LOGS
# (Check terminal where uvicorn is running)

# RESTART (if needed)
# Ctrl+C to stop, then restart uvicorn
```

**Emergency Checklist:**
- [ ] Is backend running? `curl http://localhost:8000/health`
- [ ] Is .env file present? `ls backend/.env`
- [ ] Is API key set? Check health endpoint
- [ ] Are dependencies installed? `pip list | grep openai`
- [ ] Is OpenAI service up? https://status.openai.com/
- [ ] Are there errors in logs? Check uvicorn output

---

For detailed setup instructions, see `OPENAI_SETUP_GUIDE.md`
