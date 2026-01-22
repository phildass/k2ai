# K2AI Quick Start Guide - Live AI Assistant

## 🚀 Get Your Live AI Assistant Running in 5 Minutes

This guide will get you from zero to a fully functional, live AI-powered chatbot connected to OpenAI.

## Prerequisites

- ✅ Python 3.8+ installed
- ✅ OpenAI account with API key
- ✅ 5 minutes of your time

## Step 1: Get Your OpenAI API Key (2 minutes)

1. Visit https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-` or `sk-`)
5. Keep it safe - you won't see it again!

**Don't have credits?** Add a payment method at https://platform.openai.com/account/billing

## Step 2: Install Dependencies (1 minute)

```bash
cd backend
pip install -r requirements.txt
```

## Step 3: Configure API Key (1 minute)

```bash
# Copy example environment file
cp .env.example .env

# Edit the file (use nano, vim, or any editor)
nano .env

# Replace the placeholder:
# FROM: OPENAI_API_KEY=your_openai_api_key_here
# TO:   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Save and exit (Ctrl+X, then Y, then Enter in nano)
```

## Step 4: Verify Setup (30 seconds)

```bash
python test_openai_connection.py
```

You should see:
```
✓ OpenAI API key is configured
✓ Successfully connected to OpenAI API!
✓ Live AI assistant is working!
```

❌ **Got errors?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Step 5: Start the Server (30 seconds)

```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
✓ OpenAI API key loaded successfully
✓ Using model: gpt-4-turbo-preview
✓ Live AI assistant is enabled
```

## Step 6: Test It! (30 seconds)

In a new terminal:

```bash
# Test predefined Q&A (instant, free)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'

# Test live AI (2-5 seconds, uses OpenAI)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top 3 PR trends for 2026?"}'
```

Look for `"source": "llm"` in the second response - that means live AI is working! 🎉

## Optional: Web Interface

```bash
# In repository root directory
python -m http.server 8080
```

Open browser to: http://localhost:8080/chat.html

## What You Can Ask

### Predefined Q&A (Instant, Free)
- "What services do you offer?"
- "How can I contact K2 Communications?"
- "Do you provide crisis management?"
- "What industries do you serve?"
- "What is your pricing?"

### Live AI (2-5 seconds, ~$0.01 per question)
- "What are emerging PR trends?"
- "How can AI help with crisis management?"
- "Give me 5 tips for media relations"
- "Explain the difference between traditional and digital PR"
- Anything else!

## System Status

Check if everything is working:

```bash
curl http://localhost:8000/health | python -m json.tool
```

Should show:
```json
{
  "status": "healthy",
  "api": {
    "openai_configured": true,
    "live_ai": true
  }
}
```

## Cost Management

- **Predefined answers**: FREE (90% of common questions)
- **Live AI with GPT-4**: ~$0.01 per conversation
- **Live AI with GPT-3.5**: ~$0.001 per conversation

To use cheaper GPT-3.5:
```env
# In .env file
LLM_MODEL=gpt-3.5-turbo
```

Set spending limits at https://platform.openai.com/account/limits

## Troubleshooting

### "API key is missing"
→ Check your .env file exists and has the real key (not placeholder)

### "Invalid API key"
→ Verify key on https://platform.openai.com/api-keys

### "Rate limit exceeded"
→ Add credits at https://platform.openai.com/account/billing

### Other issues?
→ See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions

## Next Steps

1. ✅ Test with different questions
2. ✅ Monitor usage at https://platform.openai.com/usage
3. ✅ Read [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md) for advanced configuration
4. ✅ Set usage limits to control costs
5. ✅ Add more predefined Q&A to reduce API calls

## Need Help?

1. Run diagnostics: `python test_openai_connection.py`
2. Check logs in the uvicorn terminal
3. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. Review [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md)

## Full Documentation

- 📘 **Setup Guide**: [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md)
- 🔧 **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- ✅ **Verification**: [DEMO_VERIFICATION.md](DEMO_VERIFICATION.md)
- 📊 **Summary**: [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)
- 📖 **Main Docs**: [README.md](README.md)

---

**That's it!** You now have a live AI assistant powered by OpenAI. 🎉

Your chatbot can:
- ✅ Answer common questions instantly (predefined Q&A)
- ✅ Generate intelligent responses for unique questions (live AI)
- ✅ Maintain conversation context
- ✅ Handle errors gracefully
- ✅ Work even if OpenAI is temporarily unavailable

**Happy chatting!** 🤖
