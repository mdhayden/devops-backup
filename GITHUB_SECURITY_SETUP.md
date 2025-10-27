# 🔒 GitHub Branch Protection Setup Guide

## 🎯 Goal: Require Manual Approval for Main Branch Merges

This will ensure that NO ONE can merge to main without your explicit approval, protecting your production deployment.

## 📋 Step-by-Step Setup:

### 1. Go to Branch Protection Settings
1. Navigate to: https://github.com/MarioH88/devops-backup/settings/branches
2. Click "Add rule" or "Add branch protection rule"

### 2. Configure Protection Rule
**Branch name pattern:** `main`

**Required Settings to Enable:**
- ✅ **Restrict pushes that create files that match this rule**
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**: Set to `1` (or more)
  - ✅ **Dismiss stale reviews when new commits are pushed**
  - ✅ **Require review from code owners** (optional)
  - ✅ **Restrict reviews to code owners** (optional)
- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (optional, but recommended)
- ✅ **Require linear history** (optional)
- ✅ **Include administrators** (IMPORTANT: This applies rules to you too)

### 3. Save Protection Rule
Click "Create" to save the protection rule.

## 🔄 New Workflow for Collaborators:

### Before (Unsafe):
```bash
git commit -m "Changes"
git push origin main  # ❌ This will be blocked
```

### After (Secure):
```bash
# Collaborator creates feature branch
git checkout -b feature/new-changes
git commit -m "Changes"
git push origin feature/new-changes

# Collaborator creates Pull Request on GitHub
# You review and approve manually
# Then merge is allowed
```

## 🚨 Important Security Benefits:

1. **No Direct Pushes**: Nobody can push directly to main
2. **Manual Review**: You must approve every change
3. **Code Review**: You can review all code before it goes live
4. **Audit Trail**: All changes are tracked in PR history
5. **Production Safety**: Prevents accidental production deployments

## 🎬 Demo Scenario:
1. "Let me show you our security controls"
2. Have collaborator try to push to main (will be rejected)
3. Show them creating a Pull Request instead
4. Demo your approval process
5. "This ensures production security and code quality"

## ⚙️ Optional Advanced Settings:

### CODEOWNERS File (Automatic Review Assignment):
Create `.github/CODEOWNERS` file:
```
# Global code owners
* @MarioH88

# Specific paths
/web_server.py @MarioH88
/cloudbuild.yaml @MarioH88
/.github/ @MarioH88
```

### Required Status Checks:
- Add "Deploy to Cloud Run" workflow as required check
- Ensures tests pass before merge approval

## 🔐 Result:
✅ Complete control over production deployments
✅ All changes require your explicit approval  
✅ Secure collaboration workflow
✅ Professional DevOps security practices