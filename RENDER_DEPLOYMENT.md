# Deploy Provon to Render (FREE TIER)

Render is the best free option for hosting your Ollama + Streamlit RAG application.

## Step 1: Deploy Ollama to Render

### 1.1 Create Render Account
1. Go to https://render.com
2. Sign up (free)
3. Connect your GitHub account

### 1.2 Create Web Service
1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Select **Deploy from GitHub repo**
4. Choose your `raviiiji/provon` repository
5. Configure:
   - **Name:** `provon-ollama`
   - **Environment:** `Docker`
   - **Plan:** `Free`
   - **Region:** Choose closest to you
6. Click **Create Web Service**
7. Wait for deployment (5-10 minutes)

### 1.3 Get Your Render URL
1. Go to your service dashboard
2. Copy the URL (e.g., `https://provon-ollama.onrender.com`)
3. Your Ollama API is at: `https://provon-ollama.onrender.com`

## Step 2: Update Streamlit Cloud Secrets

1. Go to https://share.streamlit.io/
2. Find your **provon** app
3. Click **⋮** → **Settings** → **Secrets**
4. Update:
   ```toml
   OLLAMA_HOST = "https://provon-ollama.onrender.com"
   ```
5. Click **Save**

## Step 3: Reboot Streamlit Cloud

1. Go to your **provon** app
2. Click **⋮** → **Reboot app**
3. Wait 2-3 minutes

## Step 4: Test

1. Open https://provon.streamlit.app/
2. Upload a document
3. Ask a question
4. Should work! ✅

## Troubleshooting

**"No models loaded"**
- Render is still downloading tinyllama (takes 5-15 minutes on first deploy)
- Wait and refresh the page

**"Connection refused"**
- Make sure Render service is running (check dashboard)
- Verify the URL is correct in Streamlit secrets

**Slow responses**
- First request loads the model (slow)
- Subsequent requests are faster
- Render free tier has limited resources

## Important Notes

- **Free tier limitations:**
  - Service spins down after 15 minutes of inactivity
  - First request after spin-down takes 30+ seconds
  - Limited to 750 hours/month (plenty for hobby use)
  - No GPU support (uses CPU)

- **Model download:**
  - tinyllama (~1GB) takes 5-10 minutes to download
  - Only happens once on first deployment
  - Subsequent deployments are faster

## Local Development

For local testing:
```powershell
ollama serve
# In another terminal:
streamlit run app.py
```

## Next Steps

If you need more resources later:
- Upgrade to Render's **Starter** plan ($7/month)
- Or use **AWS/GCP** free tier
