# Deployment Guide

## 1. Push to GitHub

### Option A: Using GitHub Web UI
1. Go to https://github.com/new
2. Create repo named `bluestock-village-api`
3. Run these commands:
```bash
cd /Users/stanzinpasang/Desktop/project
git remote add origin https://github.com/YOUR_USERNAME/bluestock-village-api.git
git push -u origin main
```

### Option B: Install GitHub CLI
```bash
brew install gh
gh auth login
gh repo create bluestock-village-api --public --source=. --push
```

## 2. Deploy Backend (FastAPI)

### Option A: Render.com (Free, Easy)
1. Go to https://render.com → New Web Service
2. Connect your GitHub repo
3. Settings:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable: `DATABASE_URL` (use Render's PostgreSQL)
   - Add Environment Variable: `USE_REDIS=true` and `REDIS_URL` (use Render's Redis)

### Option B: Railway.app
1. Go to https://railway.app → New Project → Deploy from GitHub
2. Add PostgreSQL and Redis plugins
3. Railway auto-detects and deploys

## 3. Deploy Frontend (React)

### Vercel (Recommended for React)
```bash
cd /Users/stanzinpasang/Desktop/project
cd frontend/admin && npx vercel --prod
cd ../demo-client && npx vercel --prod
```
Or connect GitHub repo to Vercel.com

Update `vercel.json` in each frontend with your actual backend URL.

## 4. Update API URL

After deploying backend, update these files with your backend URL:
- `frontend/admin/vercel.json`
- `frontend/demo-client/vercel.json`
- `frontend/admin/src/App.jsx` (change `/api/admin` to full URL)
- `frontend/demo-client/src/App.jsx` (change `/api/v1` to full URL)

## Quick Deploy Checklist
- [ ] Push code to GitHub
- [ ] Deploy backend to Render/Railway
- [ ] Add PostgreSQL & Redis to backend
- [ ] Run data import on production DB
- [ ] Deploy admin dashboard to Vercel
- [ ] Deploy demo client to Vercel
- [ ] Update API URLs in frontend code
- [ ] Test live endpoints
