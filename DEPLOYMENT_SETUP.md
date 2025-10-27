# 🚀 Automatic Deployment Setup

## Current Status: ⚠️ MANUAL DEPLOYMENT ONLY

Your GitHub Actions workflow is configured but **automatic deployment won't work** until you add the Google Cloud service account key.

## ✅ To Enable Live Changes:

### Option 1: Configure GitHub Secret (Recommended)
1. Go to: https://github.com/MarioH88/devops-backup/settings/secrets/actions
2. Click "New repository secret"
3. Name: `GCP_SA_KEY`
4. Value: Your Google Cloud service account JSON key
5. Save

### Option 2: Manual Deployment (Current Working Method)
```bash
gcloud builds submit --config=cloudbuild.yaml --project=gen-lang-client-0502058841
```

## 🎯 Live Demo Instructions

### For Manual Deployment:
1. Edit line ~451 in `web_server.py` (demo message)
2. Run: `gcloud builds submit --config=cloudbuild.yaml --project=gen-lang-client-0502058841`
3. Changes appear at: https://devops-backup-1002595611169.europe-west1.run.app

### For Automatic Deployment (After Secret Setup):
1. Edit line ~451 in `web_server.py` (demo message)
2. Run: `git add . && git commit -m "LIVE DEMO: [change]" && git push`
3. Changes automatically deploy in ~2-3 minutes

## 🔍 Current Demo Line:
File: `web_server.py` (around line 451)
```html
🚀 DEMO MESSAGE: Ready for live demo! 🚀
```

Change this text to demonstrate live DevOps pipeline!