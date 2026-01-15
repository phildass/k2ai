# OpenAI API Setup Guide for K2AI Chatbot

## Overview

This guide will help you set up the OpenAI API integration for the K2 Communications AI Chatbot to enable **live, real-time AI responses**.

## Prerequisites

- An OpenAI account
- An active OpenAI API key with available credits
- Access to the backend/.env file

## Step 1: Obtain an OpenAI API Key

### Option A: Using OpenAI's Platform (Recommended)

1. **Create an OpenAI Account**
   - Visit https://platform.openai.com/signup
   - Sign up with your email or Google account

2. **Add Payment Method**
   - Navigate to https://platform.openai.com/account/billing
   - Add a valid payment method
   - Consider setting up usage limits to control costs

3. **Generate API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Give it a descriptive name (e.g., "K2AI-Production")
   - **IMPORTANT**: Copy the key immediately - you won't be able to see it again!
   - The key will look like: `sk-proj-...` or `sk-...`

### Option B: Using Azure OpenAI (Enterprise)

1. Set up an Azure OpenAI resource in Azure Portal
2. Get your API key and endpoint from Azure
3. Note: This requires code modifications (not covered in this guide)

## Step 2: Configure the Backend

### Create the .env File

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Open the `.env` file in a text editor:
   ```bash
   nano .env
   # or
   vim .env
   # or use any text editor
   ```

4. Replace the placeholder API key with your real key:
   ```env
   # BEFORE:
   OPENAI_API_KEY=your_openai_api_key_here
   
   # AFTER:
   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_API_KEY_HERE
   ```

5. (Optional) Adjust other settings:
   ```env
   # LLM Configuration
   LLM_MODEL=gpt-4-turbo-preview    # or gpt-3.5-turbo for lower costs
   LLM_TEMPERATURE=0.7              # 0.0 = deterministic, 1.0 = creative
   LLM_MAX_TOKENS=1000              # Maximum response length
   ```

6. **Save the file** and ensure it's not committed to version control
   - The `.env` file is already in `.gitignore`
   - NEVER commit API keys to repositories

### Environment File Example

```env
# Environment Configuration
ENVIRONMENT=production

# API Keys
OPENAI_API_KEY=sk-proj-abc123def456...  # Your actual key here

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-production-domain.com

# LLM Configuration
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

## Step 3: Verify the Setup

### Method 1: Using the Test Script

Run the provided test script:

```bash
cd backend
python test_openai_connection.py
```

Expected output:
```
✓ OpenAI API key is configured
✓ Successfully connected to OpenAI API
✓ Model: gpt-4-turbo-preview
✓ Live AI assistant is working!

Sample Response:
"K2 Communications is a premier public relations agency..."
```

### Method 2: Manual Testing

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. In another terminal, test the API:
   ```bash
   # Test with a predefined question (should work without API key)
   curl -X POST http://localhost:8000/api/chat/ \
     -H "Content-Type: application/json" \
     -d '{"message": "What services do you offer?"}'
   
   # Test with a unique question (requires OpenAI API)
   curl -X POST http://localhost:8000/api/chat/ \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the latest trends in AI-powered PR?"}'
   ```

3. Check the response metadata:
   - Predefined answer: `"answer_source": "predefined"`
   - AI-generated answer: `"answer_source": "ai"` with `"source": "llm"`
   - Error: `"answer_source": "ai"` with `"source": "error"`

### Method 3: Web Interface Test

1. Start both backend and frontend
2. Navigate to http://localhost:3000 or http://localhost:8080/chat.html
3. Ask a unique question that's not in the predefined Q&A
4. Verify you get a real-time AI response

## Step 4: Troubleshooting

### Issue: "OpenAI API key is missing" Error

**Symptom**: Chat returns "I apologize, but the chatbot is not fully configured yet."

**Solutions**:
1. Check that `.env` file exists in the `backend/` directory
2. Verify the API key is not set to the placeholder value `your_openai_api_key_here`
3. Restart the backend server after updating `.env`
4. Check for typos in the environment variable name (must be `OPENAI_API_KEY`)

### Issue: "Invalid API Key" or Authentication Errors

**Symptom**: Error message about invalid authentication or 401 errors

**Solutions**:
1. Verify the API key is correct (copy it again from OpenAI platform)
2. Check that the key hasn't been revoked or deleted
3. Ensure your OpenAI account has available credits
4. Try regenerating the API key

### Issue: "Rate Limit Exceeded"

**Symptom**: Error about rate limits or quota exceeded

**Solutions**:
1. Check your usage at https://platform.openai.com/usage
2. Upgrade your OpenAI plan or add more credits
3. Implement rate limiting in your application
4. Consider using `gpt-3.5-turbo` instead of `gpt-4` for lower costs

### Issue: Slow Responses

**Symptom**: Chat takes a long time to respond

**Solutions**:
1. Use `gpt-3.5-turbo` for faster responses
2. Reduce `LLM_MAX_TOKENS` to limit response length
3. Check your network connection to OpenAI
4. Monitor OpenAI status at https://status.openai.com/

### Issue: Responses Not Using OpenAI

**Symptom**: All responses show `"answer_source": "predefined"`

**Solutions**:
1. Ask questions that aren't in the predefined Q&A list
2. Check backend logs for API errors
3. Verify the API key is loaded (check startup logs)
4. Ensure there are no firewalls blocking OpenAI API

## Security Best Practices

### 1. Protect Your API Key

- ✅ Store in `.env` file (already in `.gitignore`)
- ✅ Never commit to version control
- ✅ Use environment variables in production
- ✅ Rotate keys periodically
- ❌ Never hardcode keys in source code
- ❌ Never share keys publicly

### 2. Set Usage Limits

1. Visit https://platform.openai.com/account/limits
2. Set monthly spending limits
3. Set up alerts for unusual usage
4. Monitor usage regularly

### 3. Implement Rate Limiting

For production deployments:
- Add request rate limiting to prevent abuse
- Implement user authentication
- Monitor and log all API calls
- Set up alerts for unusual patterns

### 4. Production Deployment

When deploying to production:

```bash
# Set environment variable on your server
export OPENAI_API_KEY="your-production-key"

# Or use your platform's environment variable system
# Vercel: Add in project settings
# Railway: Add in project variables
# AWS: Use AWS Secrets Manager
# Azure: Use Azure Key Vault
```

## Cost Management

### Understanding OpenAI Pricing

- **GPT-4 Turbo**: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens
- **GPT-3.5 Turbo**: ~$0.0005 per 1K input tokens, ~$0.0015 per 1K output tokens
- 1 token ≈ 4 characters in English

### Reducing Costs

1. **Use Predefined Q&A**: The hybrid system answers common questions without API calls
2. **Optimize Token Usage**: 
   - Reduce `LLM_MAX_TOKENS` in `.env`
   - Keep system prompts concise
   - Clear conversation history for long sessions
3. **Choose the Right Model**:
   - Use GPT-3.5 Turbo for simple queries (faster and cheaper)
   - Reserve GPT-4 for complex reasoning tasks
4. **Monitor Usage**: Check https://platform.openai.com/usage regularly

### Example Cost Calculation

For a typical PR inquiry conversation:
- Input: ~200 tokens (user question + system prompt)
- Output: ~300 tokens (AI response)
- Cost with GPT-4 Turbo: ~$0.011 per conversation
- Cost with GPT-3.5 Turbo: ~$0.0005 per conversation

1,000 conversations per month:
- GPT-4 Turbo: ~$11/month
- GPT-3.5 Turbo: ~$0.50/month

## Testing Checklist

Before going live, verify:

- [ ] API key is set in `.env` file
- [ ] Backend starts without errors
- [ ] Health check endpoint responds: `curl http://localhost:8000/health`
- [ ] Predefined Q&A works (test: "What services do you offer?")
- [ ] Live AI responses work (test: "What are emerging trends in PR?")
- [ ] Error handling works (test with invalid API key)
- [ ] Frontend can communicate with backend
- [ ] CORS is configured for your domain
- [ ] Usage limits are set on OpenAI account
- [ ] Logs show successful API calls
- [ ] Response times are acceptable

## Support

### Getting Help

1. **OpenAI Support**: https://help.openai.com/
2. **API Documentation**: https://platform.openai.com/docs
3. **API Status**: https://status.openai.com/
4. **Community Forum**: https://community.openai.com/

### Logs and Debugging

Check backend logs for detailed information:

```bash
# Start backend with verbose logging
cd backend
LOG_LEVEL=DEBUG uvicorn main:app --reload --port 8000
```

Look for:
- `✓ OpenAI API key loaded successfully`
- `Calling OpenAI API...`
- Any error messages or stack traces

## Next Steps

After successful setup:

1. **Test thoroughly** with various questions
2. **Monitor costs** in the first week
3. **Add more predefined Q&A** to reduce API calls
4. **Set up monitoring** and alerts
5. **Plan for scaling** based on usage patterns
6. **Consider caching** for frequently asked questions

## Quick Reference

### Commands

```bash
# Setup
cp backend/.env.example backend/.env
nano backend/.env  # Add your API key

# Start backend
cd backend
uvicorn main:app --reload --port 8000

# Test connection
python test_openai_connection.py

# Test API
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about K2 Communications"}'
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `LLM_MODEL` | No | `gpt-4-turbo-preview` | OpenAI model to use |
| `LLM_TEMPERATURE` | No | `0.7` | Response creativity (0-1) |
| `LLM_MAX_TOKENS` | No | `1000` | Max response length |
| `CORS_ORIGINS` | No | `http://localhost:3000,...` | Allowed origins |

### Useful Links

- OpenAI Platform: https://platform.openai.com/
- API Keys: https://platform.openai.com/api-keys
- Usage Dashboard: https://platform.openai.com/usage
- Documentation: https://platform.openai.com/docs
- Pricing: https://openai.com/pricing

---

**Need help?** Check the troubleshooting section or contact your development team.
