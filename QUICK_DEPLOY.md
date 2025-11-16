# Quick Deployment to Streamlit Cloud (5 Minutes)

## Step 1: Prepare Your Code

Your code is already ready! Just make sure you have:
- ✅ `app.py`
- ✅ `rag_system.py`
- ✅ `backend_db.py`
- ✅ `base_knowledge.py`
- ✅ `document_processor.py`
- ✅ `requirements-advanced.txt`
- ✅ `data/provon_db.pkl` (your database)

## Step 2: Create GitHub Repository

### Option A: Using Git Command Line

```bash
# Navigate to your project
cd c:\Users\ravir\Desktop\my-notebooklm

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Provon - Document Q&A System"

# Create repo on GitHub first, then:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/provon.git
git push -u origin main
```

### Option B: Using GitHub Desktop (Easier)

1. Download GitHub Desktop: https://desktop.github.com
2. Click **File** → **New Repository**
3. Name: `provon`
4. Local Path: `c:\Users\ravir\Desktop\my-notebooklm`
5. Click **Create Repository**
6. Click **Publish Repository**
7. Sign in with GitHub account
8. Click **Publish**

## Step 3: Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **New app**
3. Sign in with GitHub (if not already)
4. Fill in:
   - **Repository**: `YOUR_USERNAME/provon`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **Deploy**

Wait 2-3 minutes for deployment...

## Step 4: Access Your App

Your live app URL:
```
https://provon-YOUR_USERNAME.streamlit.app
```

Share this link with anyone!

## Step 5: Update Your App

Just push changes to GitHub:

```bash
git add .
git commit -m "Update: added new features"
git push
```

Streamlit Cloud auto-deploys in ~1 minute!

---

## Common Issues

### Issue: "requirements.txt not found"
**Solution**: Rename `requirements-advanced.txt` to `requirements.txt`

```bash
mv requirements-advanced.txt requirements.txt
```

### Issue: "Module not found"
**Solution**: Make sure all Python files are in the root directory

### Issue: "Ollama connection failed"
**Solution**: This is expected! Ollama runs locally. 
- Option 1: Keep Ollama running on your machine
- Option 2: Switch to OpenAI API (see CLOUD_DEPLOYMENT.md)

### Issue: "Database file not found"
**Solution**: Make sure `data/provon_db.pkl` is committed to GitHub

```bash
git add data/provon_db.pkl
git commit -m "Add database"
git push
```

---

## Your Live App

Once deployed, you can:
- ✅ Share the link with anyone
- ✅ Access from any device
- ✅ Use on mobile/tablet
- ✅ No installation needed
- ✅ Always up-to-date

---

## Next: Custom Domain (Optional)

Want `provon.yourdomain.com` instead of the long URL?

1. Buy domain from GoDaddy/Namecheap
2. In Streamlit Cloud settings, add custom domain
3. Update DNS records
4. Done!

---

**Your Provon app is now live on the internet!** 🌐🚀
