# Provon Cloud Deployment Guide

## Architecture
- **Ollama (llama2b)**: Deployed on Railway
- **Streamlit App**: Deployed on Streamlit Cloud
- **Documents**: Uploaded by users in Streamlit Cloud

## Step 1: Deploy Ollama to Railway

### 1.1 Create Railway Account
1. Go to https://railway.app
2. Sign up (free tier available)
3. Connect your GitHub account

### 1.2 Deploy from GitHub
1. Go to https://railway.app/dashboard
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `raviiiji/provon` repository
4. Railway will auto-detect the Dockerfile
5. Wait for deployment (5-10 minutes)

### 1.3 Get Your Ollama URL
1. Go to your Railway project
2. Click on the **provon** service
3. Go to **Settings** → **Networking**
4. Copy the **Public URL** (e.g., `https://provon-production.up.railway.app`)
5. Your Ollama API endpoint is: `https://provon-production.up.railway.app`

## Step 2: Update Streamlit Cloud Secrets

1. Go to https://share.streamlit.io/
2. Find your **provon** app
3. Click **⋮** → **Settings** → **Secrets**
4. Add:
   ```toml
   OLLAMA_HOST = "https://your-railway-url"
   ```
   (Replace with your actual Railway URL)
5. Click **Save**

## Step 3: Reboot Streamlit Cloud

1. Go to your **provon** app
2. Click **⋮** → **Reboot app**
3. Wait 2-3 minutes

## Step 4: Test

1. Open https://provon.streamlit.app/
2. Upload a document (PDF, TXT, DOCX)
3. Ask a question about the document
4. It should now work with cloud Ollama! ✅

## Troubleshooting

**Error: "Ollama not running"**
- Check that Railway deployment is running
- Verify the URL is correct in Streamlit secrets
- Make sure URL doesn't have trailing slash

**Slow responses**
- First request takes longer (model loading)
- Subsequent requests are faster
- Railway free tier has limited resources

**403 Forbidden**
- Make sure you're using the correct Railway URL
- Check that Railway service is running

## Local Development

For local testing:
```powershell
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run Streamlit
streamlit run app.py
```

The app will automatically use `http://localhost:11434` for local development.

## Production Checklist

- [ ] Ollama deployed on Railway
- [ ] Railway URL added to Streamlit secrets
- [ ] Streamlit Cloud rebooted
- [ ] Test with sample document
- [ ] Verify different questions get different answers
