# Deployment Guide for K2 AI

This guide explains how to deploy the K2 AI application using Render.

## Overview

The K2 AI application is deployed at Render for both frontend and backend services.

## Prerequisites

1. Render account (sign up at https://render.com)
2. GitHub account with repository access
3. DNS access to configure custom domains (optional)
4. OpenAI API key from https://platform.openai.com/api-keys

## Deployment Steps

### 1. Deploy Backend to Render

The backend is a Python FastAPI application.

1. **Create New Web Service**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `phildass/k2ai`
   
2. **Configure Backend Service**
   - **Name**: `k2ai-backend` (or any name you prefer)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free tier or as needed

3. **Set Environment Variables**
   - In Render dashboard, go to "Environment" tab
   - Add the following environment variables:
     - **Key**: `OPENAI_API_KEY`, **Value**: Your OpenAI API key (starts with `sk-`)
     - **Key**: `ADMIN_PASSWORD`, **Value**: Your admin password
     - **Key**: `CORS_ORIGINS`, **Value**: Your frontend URL (e.g., `https://your-frontend.onrender.com`)
   - Click "Save Changes"

4. **Deploy**
   - Render will automatically deploy your backend
   - Wait for deployment to complete (check logs for any errors)
   - Your backend will be available at: `https://your-backend-name.onrender.com`

### 2. Deploy Frontend to Render

The frontend is a Next.js application.

1. **Create New Web Service**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `phildass/k2ai`
   
2. **Configure Frontend Service**
   - **Name**: `k2ai-frontend` (or any name you prefer)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `frontend`
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Instance Type**: Free tier or as needed

3. **Set Environment Variables**
   - In Render dashboard, go to "Environment" tab
   - Add the following environment variable:
     - **Key**: `NEXT_PUBLIC_API_URL`, **Value**: Your backend URL (e.g., `https://your-backend-name.onrender.com`)
   - Click "Save Changes"

4. **Deploy**
   - Render will automatically deploy your frontend
   - Wait for deployment to complete (check logs for any errors)
   - Your frontend will be available at: `https://your-frontend-name.onrender.com`

### 3. Configure Custom Domain (Optional)

**On Render:**
- Go to your service → "Settings" → "Custom Domains"
- Click "Add Custom Domain"
- Enter your custom domain (e.g., `testk2ai.unnon.ai`)
- Render will provide CNAME or A record values

**On Your DNS Provider:**
- Log in to your DNS provider (e.g., domain registrar)
- Add a CNAME record:
  - **Name/Host**: `testk2ai` (or your subdomain)
  - **Value/Target**: Your Render URL (e.g., `your-app.onrender.com`)
  - **TTL**: 3600 (or default)
- Save the DNS record

**Note:** DNS propagation can take up to 48 hours, but typically happens within minutes to hours.

### 4. Verify Deployment

1. **Backend Health Check**
   - Visit `https://your-backend-name.onrender.com/health`
   - You should see a JSON response with health status

2. **Frontend Check**
   - Visit `https://your-frontend-name.onrender.com`
   - You should see the K2 AI chatbot interface

3. **Test Integration**
   - Try sending a message in the chat interface
   - Verify the backend is responding correctly

## DNS Configuration

Configure DNS records in your DNS provider:

**For custom domain (e.g., testk2ai.unnon.ai):**

- **Type**: CNAME
- **Name**: testk2ai (or your subdomain)
- **Value**: your-app.onrender.com (provided by Render)
- **TTL**: 3600 (or automatic)

Check DNS propagation:
```bash
# Check if DNS is propagated
dig testk2ai.unnon.ai

# Or use online tools
# https://www.whatsmydns.net/#A/testk2ai.unnon.ai
```

## Environment Variables Reference

### Backend Environment Variables
- `OPENAI_API_KEY` - Required: Your OpenAI API key
- `ADMIN_PASSWORD` - Required: Admin panel password
- `CORS_ORIGINS` - Required: Allowed frontend origins
- `LLM_MODEL` - Optional: OpenAI model (default: gpt-4-turbo-preview)
- `LLM_TEMPERATURE` - Optional: Response creativity (default: 0.7)
- `LLM_MAX_TOKENS` - Optional: Max response length (default: 1000)

### Frontend Environment Variables
- `NEXT_PUBLIC_API_URL` - Required: Backend API URL

## Troubleshooting

### Backend Issues

**Service won't start**
- Check deployment logs in Render Dashboard
- Verify all environment variables are set correctly
- Ensure `requirements.txt` is present in backend directory
- Check that `OPENAI_API_KEY` is valid

**CORS errors**
- Update `CORS_ORIGINS` to include your frontend URL
- Redeploy the backend after updating environment variables

### Frontend Issues

**Build failures**
- Check Render deployment logs
- Ensure all dependencies are in `package.json`
- Verify Node.js version compatibility

**Can't connect to backend**
- Verify `NEXT_PUBLIC_API_URL` points to the correct backend URL
- Check backend is running and accessible
- Look for CORS errors in browser console

### DNS Issues

**Domain not working**
- Verify DNS configuration matches Render's instructions
- Wait for DNS propagation (can take up to 48 hours)
- Use `dig` or online tools to check propagation status

### SSL Certificate Issues

**HTTPS not working**
- Render automatically provisions SSL certificates
- May take a few minutes after DNS is configured
- Check Render dashboard for certificate status

## Monitoring and Logs

### View Logs
- Go to Render Dashboard
- Select your service
- Click on "Logs" tab
- View real-time logs and errors

### Monitor Performance
- Check service metrics in Render Dashboard
- Monitor response times and uptime
- Set up alerts for service downtime

## Important Notes

- Render free tier apps may spin down after inactivity - first request might be slow
- The server automatically uses `process.env.PORT` provided by Render
- No code changes needed for custom domain - handled by Render and DNS
- Always redeploy after updating environment variables

## Rollback

To rollback to a previous deployment:
1. Go to Render Dashboard
2. Navigate to your service
3. Click on "Deploys" tab
4. Find a previous successful deployment
5. Click "Redeploy" on that version

## Support

For deployment issues:
- Check Render documentation: https://render.com/docs
- Review deployment logs in Render Dashboard
- Contact the development team
