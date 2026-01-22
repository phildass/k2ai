# Deployment Guide

## Production Deployment

This guide covers deploying the K2 AI Chatbot to Render.

## Deployment Platform

The application is deployed on **Render** (https://render.com) for both frontend and backend services.

## Prerequisites

- Render account (sign up at https://render.com)
- GitHub account with repository access
- OpenAI API key from https://platform.openai.com/api-keys

## Quick Deploy with Render

### Step 1: Deploy Backend (FastAPI)

1. **Create New Web Service**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `phildass/k2ai`

2. **Configure Backend Service**
   - **Name**: `k2ai-backend`
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `ADMIN_PASSWORD` - Your admin password
   - `CORS_ORIGINS` - Your frontend URL
   - `LLM_MODEL` - (Optional) gpt-4-turbo-preview
   - `LLM_TEMPERATURE` - (Optional) 0.7
   - `LLM_MAX_TOKENS` - (Optional) 1000

4. **Deploy**
   - Render will automatically deploy
   - Your backend URL: `https://your-backend-name.onrender.com`

### Step 2: Deploy Frontend (Next.js)

1. **Create New Web Service**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `phildass/k2ai`

2. **Configure Frontend Service**
   - **Name**: `k2ai-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`

3. **Set Environment Variables**
   - `NEXT_PUBLIC_API_URL` - Your backend URL from Step 1

4. **Deploy**
   - Render will automatically deploy
   - Your frontend URL: `https://your-frontend-name.onrender.com`

## Docker Deployment

For deploying with Docker on Render or any other platform:

### Build Images

```bash
# Frontend
cd frontend
docker build -t k2ai-frontend .

# Backend
cd backend
docker build -t k2ai-backend .
```

### Deploy with Docker Compose

```bash
# On your server
git clone https://github.com/phildass/k2ai.git
cd k2ai

# Set up environment variables
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit environment files
nano backend/.env
nano frontend/.env.local

# Deploy with Docker Compose
docker-compose up -d --build
```

## Environment Variables Checklist

### Backend (Production)
- [ ] `OPENAI_API_KEY` - OpenAI API key
- [ ] `ADMIN_PASSWORD` - Admin panel password
- [ ] `ENVIRONMENT` - Set to "production"
- [ ] `CORS_ORIGINS` - Frontend URL(s)
- [ ] `LLM_MODEL` - GPT model to use
- [ ] `LLM_TEMPERATURE` - Response randomness
- [ ] `LLM_MAX_TOKENS` - Max response length

### Frontend (Production)
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL

## Custom Domain Configuration

### On Render

1. Go to your service → "Settings" → "Custom Domains"
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `k2ai.example.com`)
4. Render will provide DNS configuration

### On Your DNS Provider

Add a CNAME record:
- **Type**: CNAME
- **Name**: Your subdomain (e.g., `k2ai`)
- **Value**: Your Render URL (e.g., `your-app.onrender.com`)
- **TTL**: 3600

## Post-Deployment Testing

### 1. Test Backend Health

```bash
# Health check
curl https://your-backend-url.onrender.com/health

# Test chat endpoint
curl -X POST https://your-backend-url.onrender.com/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'
```

### 2. Test Frontend

- Visit your frontend URL
- Verify the chat interface loads
- Send a test message
- Check backend integration

### 3. Test Custom Domain

- Visit your custom domain
- Verify SSL certificate is active
- Test all functionality

## Monitoring and Logging

### View Logs on Render

1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. View real-time logs and errors

### Key Metrics to Monitor

- API response times
- Error rates
- Service uptime
- Resource usage

## Security Checklist

- [ ] HTTPS enabled (automatic on Render)
- [ ] Environment variables secured
- [ ] CORS properly configured
- [ ] API keys not exposed in code
- [ ] Admin password set and secure

## Troubleshooting

### Backend Service Won't Start

**Check:**
- Deployment logs for errors
- Environment variables are set correctly
- `requirements.txt` is present and valid
- OpenAI API key is valid

### Frontend Can't Connect to Backend

**Check:**
- `NEXT_PUBLIC_API_URL` is set correctly
- Backend service is running
- CORS_ORIGINS includes frontend URL
- Network connectivity

### Build Failures

**Backend:**
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`
- Review build logs

**Frontend:**
- Check Node.js version compatibility
- Verify all dependencies in `package.json`
- Clear build cache and retry

### DNS Issues

- Verify DNS configuration matches Render's instructions
- Wait for DNS propagation (up to 48 hours)
- Use `dig` command to check DNS status:
  ```bash
  dig your-domain.com
  ```

## Rollback Procedure

If deployment fails:

1. Go to Render Dashboard
2. Select your service
3. Click "Deploys" tab
4. Find previous successful deployment
5. Click "Redeploy"

## Backup and Maintenance

### Regular Maintenance

- Monitor service health regularly
- Check logs for errors
- Update dependencies periodically
- Review security alerts

### Database Backup (Future)

When database is added:
- Set up automated backups
- Test restore procedures
- Document backup schedule

## Cost Management

### Render Pricing

- **Free Tier**: Available for testing
- **Paid Plans**: Scale as needed
- Monitor usage in Render dashboard

### Tips to Reduce Costs

- Use predefined Q&A to reduce API calls
- Optimize token usage
- Monitor OpenAI API usage
- Set usage limits on OpenAI account

## Support

For deployment issues:
- Check Render documentation: https://render.com/docs
- Review deployment logs
- Contact development team
