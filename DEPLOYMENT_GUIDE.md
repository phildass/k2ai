# Deployment Guide for testk2ai.unnon.ai

This guide explains how to deploy the K2 AI test page to testk2ai.unnon.ai.

## Overview

The test page is a simple HTML page with the title "Testing page for K2 AI" deployed at the custom domain testk2ai.unnon.ai.

## Quick Start - Simple Static Deployment

For the simplest deployment option, use the `index.html` file in the root directory:

1. Upload `index.html` to any static hosting service (Vercel, Netlify, GitHub Pages, etc.)
2. Configure custom domain to point to testk2ai.unnon.ai
3. Done!

## Full Application Deployment

For deploying the full Next.js application:

## Prerequisites

1. Vercel account with access to deploy
2. DNS access to configure the unnon.ai domain
3. GitHub repository connected to Vercel
4. Vercel access token for automated deployments (optional, for GitHub Actions)

## Deployment Steps

### 1. Deploy to Vercel

#### Option A: Via Vercel CLI
```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Navigate to the project root
cd /path/to/k2ai

# Deploy to Vercel
vercel --prod
```

#### Option B: Via Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import the `phildass/k2ai` repository
4. Configure:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Click "Deploy"

### 2. Configure Custom Domain

After initial deployment:

1. Go to your project in Vercel Dashboard
2. Navigate to Settings → Domains
3. Add custom domain: `testk2ai.unnon.ai`
4. Vercel will provide DNS records to configure

### 3. DNS Configuration

Configure the following DNS records in your unnon.ai DNS provider:

**For testk2ai.unnon.ai:**

- **Type**: CNAME
- **Name**: testk2ai
- **Value**: cname.vercel-dns.com
- **TTL**: 3600 (or automatic)

OR

- **Type**: A
- **Name**: testk2ai
- **Value**: 76.76.21.21 (Vercel's IPv4)
- **TTL**: 3600

**Additional AAAA record for IPv6 (optional):**
- **Type**: AAAA
- **Name**: testk2ai
- **Value**: 2606:4700:10::6816:1515 (Vercel's IPv6)

### 4. Verify Deployment

1. Wait for DNS propagation (can take up to 48 hours, usually much faster)
2. Visit https://testk2ai.unnon.ai
3. You should see the test page with "Testing page for K2 AI"

#### Check DNS propagation:
```bash
# Check if DNS is propagated
dig testk2ai.unnon.ai

# Or use online tools
# https://www.whatsmydns.net/#A/testk2ai.unnon.ai
```

## Troubleshooting

### Automated Deployment (GitHub Actions)

A GitHub Actions workflow is configured in `.github/workflows/deploy.yml` for automated deployment. To use it:

1. In your GitHub repository, go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `VERCEL_TOKEN`: Your Vercel access token (from Vercel Account Settings → Tokens)
   - `VERCEL_ORG_ID`: Your Vercel organization ID (found in `.vercel/project.json` after running `vercel link`)
   - `VERCEL_PROJECT_ID`: Your Vercel project ID (found in `.vercel/project.json` after running `vercel link`)

3. The workflow will automatically deploy on push to `main` branch or the deployment branch.

To get your organization and project IDs:
```bash
cd frontend
vercel link
cat .vercel/project.json
```

## Troubleshooting

### Domain not working
- Check DNS configuration
- Verify CNAME/A record is correct
- Wait for DNS propagation (use `dig` or `nslookup` to check)
- Check Vercel dashboard for domain status

### Build failures
- Check Vercel deployment logs
- Ensure all dependencies are in package.json
- Verify Node.js version compatibility

### SSL Certificate issues
- Vercel automatically provisions SSL certificates
- May take a few minutes after DNS is configured
- Check Vercel dashboard for certificate status

## Environment Variables

For this simple test page, no environment variables are required. The page is static and doesn't connect to the backend API.

## Rollback

To rollback to a previous version:
1. Go to Vercel Dashboard
2. Navigate to Deployments
3. Select a previous deployment
4. Click "Promote to Production"

## Additional Notes

- The current deployment is a simple test page
- To deploy the full K2 AI application, revert the changes to `frontend/src/app/page.tsx`
- The backend API is not included in this deployment (frontend only)
- For production deployment with backend, see the main README.md

## Support

For deployment issues:
- Check Vercel documentation: https://vercel.com/docs
- Review deployment logs in Vercel Dashboard
- Contact the development team
