# 🚀 AUTOMATIC DEPLOYMENT SETUP

## ✅ I've Updated Your Workflow!

Your GitHub Actions will now automatically deploy when you push to main.

## 🔑 CRITICAL: Configure GitHub Secret

**You MUST add the GCP service account key to GitHub for this to work:**

### Step 1: Get Your Service Account Key
```powershell
# Create a service account key (if you don't have one)
gcloud iam service-accounts create github-actions --display-name="GitHub Actions"

# Add required roles
gcloud projects add-iam-policy-binding gen-lang-client-0502058841 \
    --member="serviceAccount:github-actions@gen-lang-client-0502058841.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding gen-lang-client-0502058841 \
    --member="serviceAccount:github-actions@gen-lang-client-0502058841.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding gen-lang-client-0502058841 \
    --member="serviceAccount:github-actions@gen-lang-client-0502058841.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

# Create and download the key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions@gen-lang-client-0502058841.iam.gserviceaccount.com
```

### Step 2: Add Secret to GitHub
1. Go to: https://github.com/MarioH88/devops-backup/settings/secrets/actions
2. Click "New repository secret"
3. Name: `GCP_SA_KEY`
4. Value: Copy the ENTIRE contents of `github-actions-key.json`
5. Click "Add secret"

## 🎯 After Setup - Automatic Workflow:

```bash
# Edit any file
# Commit changes
git add .
git commit -m "Live demo change"
git push origin main

# GitHub Actions automatically:
# 1. Builds Docker image
# 2. Pushes to Container Registry  
# 3. Deploys to Cloud Run
# 4. Your changes go live in ~2-3 minutes!
```

## 🔍 Verify It's Working:
1. Make a small change to web_server.py
2. Commit and push
3. Check: https://github.com/MarioH88/devops-backup/actions
4. Watch the deployment happen automatically!

## 📱 Test Command:
```powershell
# Quick test after setup
git add .github/workflows/deploy.yml
git commit -m "Enable automatic deployment"
git push origin main
# Should trigger automatic build!
```