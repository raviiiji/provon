# Git Credentials Setup Guide

## Step 1: Create GitHub Repository First

1. Go to https://github.com/new
2. Create new repository:
   - **Name**: `provon`
   - **Description**: `Provon - Document Q&A System with AI`
   - **Public** (not private)
3. Click **"Create repository"**
4. You'll see a page with instructions - copy the HTTPS URL

---

## Step 2: Configure Git Credentials (Windows)

### Option A: Using Git Credential Manager (Easiest)

```powershell
# Configure credential helper
git config --global credential.helper manager-core

# Or use wincred
git config --global credential.helper wincred
```

### Option B: Store Token in Git Config

```powershell
# Replace YOUR_TOKEN with your actual token
git config --global credential.https://github.com.username raviiiji
git config --global credential.https://github.com.helper manager-core
```

---

## Step 3: Push Your Code to GitHub

```powershell
# Navigate to your project
cd c:\Users\ravir\Desktop\my-notebooklm

# Check git status
git status

# You should see all files ready to commit
# If not already committed, do:
git add .
git commit -m "Provon - Document Q&A System"

# Set remote (replace with your repo URL from GitHub)
git remote add origin https://github.com/raviiiji/provon.git

# Push to GitHub
git push -u origin main
```

---

## Step 4: When Git Asks for Credentials

When you run `git push`, you'll see a popup or prompt:

### On Windows with Credential Manager:
1. A popup window will appear
2. Enter:
   - **Username**: `raviiiji`
   - **Password**: Your GitHub token: `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`
3. Check "Remember this password"
4. Click OK

### If Popup Doesn't Appear:
Git will prompt in the terminal:
```
Username for 'https://github.com': raviiiji
Password for 'https://raviiiji@github.com': [paste your token here]
```

---

## Step 5: Verify Push Was Successful

```powershell
# Check if remote is set correctly
git remote -v

# You should see:
# origin  https://github.com/raviiiji/provon.git (fetch)
# origin  https://github.com/raviiiji/provon.git (push)

# Check git log
git log --oneline

# You should see your commits
```

---

## Complete Command Sequence

Copy and run these commands one by one:

```powershell
# 1. Navigate to project
cd c:\Users\ravir\Desktop\my-notebooklm

# 2. Configure git
git config --global credential.helper manager-core

# 3. Check status
git status

# 4. If changes exist, commit them
git add .
git commit -m "Provon deployment ready"

# 5. Add remote (use your GitHub repo URL)
git remote add origin https://github.com/raviiiji/provon.git

# 6. Push to GitHub
git push -u origin main
```

When prompted, enter:
- **Username**: `raviiiji`
- **Password**: `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`

---

## Troubleshooting

### Error: "fatal: remote origin already exists"

```powershell
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/raviiiji/provon.git
```

### Error: "Repository not found"

1. Make sure you created the repo on GitHub first
2. Check the URL is correct: `https://github.com/raviiiji/provon.git`
3. Make sure repo is PUBLIC (not private)

### Error: "Authentication failed"

1. Check your token is correct
2. Make sure token has `repo` scope
3. Try clearing cached credentials:

```powershell
# Clear cached credentials
git credential reject https://github.com

# Then try pushing again
git push -u origin main
```

### Token Expired

If your token expires, generate a new one:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Copy the new token
4. Clear old credentials and use new token

---

## After Successful Push

Once your code is on GitHub:

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Select:
   - Repository: `raviiiji/provon`
   - Branch: `main`
   - Main file: `app.py`
4. Click **Deploy**

Your live app: `https://provon-raviiiji.streamlit.app`

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git config --global credential.helper manager-core` | Enable credential manager |
| `git remote add origin URL` | Add GitHub repository |
| `git push -u origin main` | Push code to GitHub |
| `git remote -v` | View remote URLs |
| `git status` | Check git status |
| `git log --oneline` | View commit history |

---

## Your Token (Keep Safe!)

⚠️ **Never commit your token to GitHub!**
- Store it locally only
- Use Git Credential Manager to handle it
- Never paste it in files

---

**Ready to deploy?** Follow the steps above! 🚀
