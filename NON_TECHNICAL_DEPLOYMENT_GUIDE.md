# Node.js Deployment Checklist for Non-Technical Team Members

## Before Each Deployment

### 1. Check Your Code
- [ ] All your changes are saved
- [ ] You tested the website/app on your computer
- [ ] No error messages appear when you run `npm start`

### 2. Verify Files
- [ ] You did NOT add a `node_modules` folder to git
- [ ] You did NOT add `.env` files to git (these contain secrets!)
- [ ] You DID update `package.json` if you added new code libraries

### 3. Run These Commands (in order)

```bash
# Step 1: Install everything fresh
npm install

# Step 2: Start the app
npm start

# Step 3: Check if it works (open in browser)
http://localhost:3000/health
```

**What should happen:**
- No red error messages
- The health page shows `"status": "healthy"`
- No warnings about missing files or modules

## Deploying to Render

### Step-by-Step Guide

#### Step 1: Commit Your Code
```bash
git add .
git commit -m "Brief description of what you changed"
git push
```

#### Step 2: Open Render Dashboard
1. Go to https://dashboard.render.com
2. Log in with K2 Communications account
3. Find the "k2ai" service
4. Click on it

#### Step 3: Deploy
**Option A: Automatic (recommended)**
- If you pushed to the main branch, it will deploy automatically
- Wait 2-5 minutes for the deployment to complete

**Option B: Manual**
1. Click the "Manual Deploy" button
2. Select "Deploy latest commit"
3. Click "Deploy"
4. Wait 2-5 minutes

#### Step 4: Check If It Worked
After deployment completes:

1. Click "Open" button (top right)
2. Your website should load
3. Add `/health` to the URL to check health status
   - Example: `https://k2ai.onrender.com/health`
   - Should show: `{"status":"healthy",...}`

## Common Problems & Solutions

### Problem: "Cannot find module" Error
**Solution:**
1. Go to Render Dashboard
2. Click "Settings" tab
3. Scroll down to "Clear Build Cache"
4. Click the button
5. Go back to "Manual Deploy" and deploy again

### Problem: App Won't Start
**Check these:**
- [ ] Is `OPENAI_API_KEY` set in Render Environment Variables?
- [ ] Is the Start Command set to `node index.js`?
- [ ] Did you clear the build cache?

**How to check environment variables:**
1. Go to Render Dashboard → k2ai service
2. Click "Environment" tab
3. Verify `OPENAI_API_KEY` exists
4. If not, click "Add Environment Variable"

### Problem: Git Won't Let Me Push
**Common causes:**
- You have changes you haven't committed
- Someone else changed the same files

**Solution:**
```bash
# See what changed
git status

# Save your changes first
git stash

# Get latest changes from others
git pull

# Apply your changes back
git stash pop

# If there are conflicts, ask for help!
```

### Problem: Local Server Won't Start
**Solution:**
```bash
# Stop any running servers
# Press Ctrl+C in the terminal

# Delete old files
rm -rf node_modules

# Reinstall everything
npm install

# Try starting again
npm start
```

## DO NOT Do These Things! ❌

### Never Commit These Files:
- `node_modules/` folder
- `.env` file
- `package-lock.json` (unless you changed dependencies)
- Any files with passwords or API keys

### Never Do These Actions:
- Push directly to `main` branch without testing
- Delete `package.json` or `.gitignore`
- Change Node.js version without asking
- Remove dependencies from `package.json` unless you're sure

## Quick Reference Card

### Is Everything Ready to Deploy?
Run this checklist:
```bash
# 1. Is git clean?
git status
# Should say "nothing to commit, working tree clean"

# 2. Do dependencies work?
npm install
# Should say "added X packages" with no errors

# 3. Does the app start?
npm start
# Should say "K2 AI Server running on port 3000"

# 4. Does the health check work?
curl http://localhost:3000/health
# Should return JSON with "status": "healthy"
```

If all 4 steps work → **Safe to deploy!** ✅

## Getting Help

### Before Asking for Help:
1. Copy the error message (the full red text)
2. Take a screenshot of what you see
3. Note what you were trying to do

### Where to Ask:
- GitHub Issues: Create an issue with the `help` tag
- Team Chat: Post in #development or #tech-support
- Email: Include "K2AI Deployment Help" in subject

### What to Include:
- What you were trying to do
- What command you ran
- The error message (copy the full text)
- Screenshot of the problem
- What you already tried to fix it

## Glossary (Simple Terms)

- **npm**: Tool for managing code libraries
- **node_modules**: Folder with code libraries (never commit this!)
- **package.json**: List of libraries your app needs
- **.env**: File with secrets (never share this!)
- **Deploy**: Put your code online so others can use it
- **Build**: Prepare your code to run online
- **Environment Variable**: Secret setting (like API keys)
- **Health Check**: Test URL to see if app is running

## Emergency Contacts

### If Nothing Works:
1. Don't panic!
2. Stop the deployment if possible
3. Contact the technical lead
4. Document what happened
5. Wait for help before trying again

### Rollback (Undo a Deployment)
If the deployment broke the website:
1. Go to Render Dashboard
2. Click on the deployment that worked before
3. Click "Redeploy"
4. Wait for it to finish

---
**Remember:** It's okay to ask for help! Better to ask than to break production. 🙂

**Last Updated:** January 23, 2026
