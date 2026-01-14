# Deployment Guide

## Production Deployment

This guide covers deploying the K2 AI Chatbot to production environments.

## Quick Deploy Options

### Option 1: Vercel (Frontend) + Railway (Backend)

**Recommended for fastest deployment**

#### Frontend to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy frontend:
```bash
cd frontend
vercel --prod
```

3. Set environment variables in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

#### Backend to Railway

1. Create new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set root directory to `backend/`
4. Add environment variables:
```
OPENAI_API_KEY=your-key
CORS_ORIGINS=https://your-frontend.vercel.app
```
5. Deploy

### Option 2: Docker on Any Cloud Provider

#### Build Images

```bash
# Frontend
cd frontend
docker build -t k2ai-frontend .

# Backend
cd backend
docker build -t k2ai-backend .
```

#### Deploy to AWS ECS, Azure Container Instances, or GCP Cloud Run

Follow provider-specific instructions for container deployment.

## Detailed Deployment Instructions

### Vercel (Frontend)

**Prerequisites**: Vercel account

**Steps**:

1. **Connect Repository**
   - Go to [Vercel Dashboard](https://vercel.com)
   - Import your GitHub repository
   - Select the `frontend` directory as root

2. **Configure Build**
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-app.vercel.app`

### Railway (Backend)

**Prerequisites**: Railway account

**Steps**:

1. **Create New Project**
   - Go to [Railway](https://railway.app)
   - Create new project from GitHub repo

2. **Configure Service**
   - Root Directory: `backend/`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   ```
   OPENAI_API_KEY=sk-...
   LLM_MODEL=gpt-4-turbo-preview
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Generate Domain**
   - Railway will provide a public URL
   - Update frontend's `NEXT_PUBLIC_API_URL` to this URL

### Render (Backend Alternative)

1. **Create Web Service**
   - Connect GitHub repository
   - Root Directory: `backend`
   - Environment: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   - Add all required variables from `.env.example`

### AWS Deployment

#### Using EC2

**Backend**:
```bash
# On EC2 instance
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Clone repo
git clone https://github.com/phildass/k2ai.git
cd k2ai/backend

# Install dependencies
pip3 install -r requirements.txt

# Set up environment
nano .env  # Add your environment variables

# Run with systemd
sudo nano /etc/systemd/system/k2ai-backend.service
```

**systemd service file**:
```ini
[Unit]
Description=K2 AI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/k2ai/backend
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start k2ai-backend
sudo systemctl enable k2ai-backend
```

**Frontend**:
```bash
# On EC2 instance or use Vercel
sudo apt install nodejs npm nginx

cd /home/ubuntu/k2ai/frontend
npm install
npm run build

# Serve with nginx
sudo nano /etc/nginx/sites-available/k2ai-frontend
```

**nginx config**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Using ECS (Docker)

1. **Push images to ECR**
```bash
aws ecr create-repository --repository-name k2ai-frontend
aws ecr create-repository --repository-name k2ai-backend

# Tag and push
docker tag k2ai-frontend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/k2ai-frontend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/k2ai-frontend:latest
```

2. **Create ECS task definitions** for frontend and backend

3. **Deploy to ECS cluster**

### Azure Deployment

#### Using App Service

**Backend**:
```bash
az webapp create --resource-group k2ai-rg --plan k2ai-plan --name k2ai-backend --runtime "PYTHON:3.11"
az webapp config appsettings set --resource-group k2ai-rg --name k2ai-backend --settings OPENAI_API_KEY="your-key"
```

**Frontend**:
```bash
az staticwebapp create --name k2ai-frontend --resource-group k2ai-rg --source https://github.com/phildass/k2ai --branch main --app-location "/frontend"
```

### Google Cloud Platform

#### Using Cloud Run

**Backend**:
```bash
gcloud run deploy k2ai-backend \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key
```

**Frontend**:
```bash
gcloud run deploy k2ai-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://backend-url
```

## Docker Compose Deployment

For deploying both services together:

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
- [ ] `ENVIRONMENT=production`
- [ ] `CORS_ORIGINS` - Frontend URL(s)
- [ ] `LLM_MODEL` - GPT model to use
- [ ] `LLM_TEMPERATURE` - Response randomness
- [ ] `LLM_MAX_TOKENS` - Max response length

### Frontend (Production)
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL

## Post-Deployment

### 1. Test All Endpoints
```bash
# Health check
curl https://your-backend-url.com/health

# Test chat
curl -X POST https://your-backend-url.com/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'
```

### 2. Set Up Monitoring

- Enable logging
- Set up error tracking (Sentry, etc.)
- Monitor API usage
- Set up uptime monitoring

### 3. Configure Custom Domain

- Point domain to deployment
- Set up SSL/TLS certificates
- Update environment variables

### 4. Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] API keys rotated regularly
- [ ] No secrets in code

## Scaling Considerations

### Horizontal Scaling
- Use load balancer for multiple instances
- Add database for conversation persistence
- Implement Redis for session management

### Vertical Scaling
- Increase instance size for backend (more memory for LLM)
- Optimize frontend bundle size

## Backup and Recovery

### Database Backup
When database is added:
- Regular automated backups
- Point-in-time recovery
- Backup verification

### Code Backup
- GitHub as source of truth
- Tag releases
- Document deployment procedures

## Monitoring and Logging

### Recommended Tools
- **Logging**: CloudWatch, Stackdriver, or Papertrail
- **Monitoring**: New Relic, Datadog, or Prometheus
- **Error Tracking**: Sentry
- **Uptime**: UptimeRobot, Pingdom

### Key Metrics to Monitor
- API response times
- Error rates
- LLM token usage
- User engagement
- Conversation completion rates

## Rollback Procedure

If deployment fails:

1. **Vercel**: Click "Rollback" in dashboard
2. **Railway**: Redeploy previous commit
3. **Docker**: `docker-compose down && git checkout previous-tag && docker-compose up -d`

## Support

For deployment issues:
- Check logs in your platform's dashboard
- Review environment variables
- Verify API keys are valid
- Check CORS configuration
