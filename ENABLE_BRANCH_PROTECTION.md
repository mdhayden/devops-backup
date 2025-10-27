# Enable Branch Protection Rules

To require manual approval for all changes (including your own), follow these steps:

## 1. Go to Branch Protection Settings
Visit: https://github.com/MarioH88/devops-backup/settings/branches

## 2. Add Rule for `main` Branch
Click **"Add rule"** and configure:

### Branch Name Pattern: 
```
main
```

### Required Settings:
- ✅ **Require a pull request before merging**
  - ✅ Require approvals: **1**
  - ✅ **Dismiss stale PR approvals when new commits are pushed**
  - ✅ **Require review from code owners** (this uses CODEOWNERS file)
  
- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging

- ✅ **Require conversation resolution before merging**

- ✅ **Include administrators** (This makes the rule apply to you too!)

### Advanced Settings:
- ✅ **Allow force pushes** → **Nobody** (for safety)
- ✅ **Allow deletions** → **Nobody** (for safety)

## 3. Save Protection Rule
Click **"Create"** to enable the protection.

## Result:
After enabling this:
1. **Nobody (including you) can push directly to main**
2. **All changes must go through Pull Requests**
3. **You must manually approve each PR**
4. **Auto-deployment happens after merge**

## Workflow:
1. Make changes in a feature branch
2. Create Pull Request
3. Review and approve your own PR
4. Merge PR → Auto-deploy

This gives you full control over what gets deployed!