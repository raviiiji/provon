# Provon Cloud Deployment Guide

Deploy your Provon app to the cloud and access it from anywhere!

## Option 1: Streamlit Cloud (Easiest) ⭐ RECOMMENDED

### Step 1: Push to GitHub

1. Create a GitHub account (if you don't have one): https://github.com
2. Create a new repository called `provon`
3. Push your code:

```bash
cd c:\Users\ravir\Desktop\my-notebooklm
git init
git add .
git commit -m "Initial Provon deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/provon.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Sign in with GitHub
4. Select:
   - Repository: `YOUR_USERNAME/provon`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Deploy**

### Step 3: Access Your App

Your app will be live at:
```
https://provon-YOUR_USERNAME.streamlit.app
```

**Pros:**
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Auto-updates on GitHub push
- ✅ Custom domain support

**Cons:**
- ⚠️ Ollama must be running on your local machine (won't work with cloud Ollama)
- ⚠️ Limited to Streamlit's free tier resources

---

## Option 2: Heroku (With Ollama Support)

### Step 1: Create Heroku Account

1. Sign up at https://www.heroku.com
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Create Procfile

Create `Procfile` in your project root:

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 3: Create requirements.txt

```bash
pip freeze > requirements.txt
```

### Step 4: Deploy

```bash
heroku login
heroku create provon-app
git push heroku main
```

Your app will be at: `https://provon-app.herokuapp.com`

---

## Option 3: AWS (Most Powerful)

### Using AWS Elastic Beanstalk

1. Install AWS CLI
2. Create `.ebextensions/python.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
```

3. Deploy:

```bash
eb init -p python-3.9 provon
eb create provon-env
eb deploy
```

Your app will be at: `https://provon-env.elasticbeanstalk.com`

---

## Option 4: Google Cloud Run (Recommended for Scalability)

### Step 1: Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Deploy

```bash
gcloud run deploy provon \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Your app will be at: `https://provon-XXXXX.run.app`

---

## Option 5: Custom Domain

### For Streamlit Cloud

1. Go to your app settings
2. Click **Settings** → **Custom domain**
3. Enter your domain (e.g., `provon.yourdomain.com`)
4. Update DNS records as instructed

### For Other Platforms

Use a domain registrar like:
- GoDaddy
- Namecheap
- Google Domains

Then point your domain to your cloud app.

---

## Important: Ollama Configuration

### Problem
Ollama runs locally on your machine. Cloud apps can't access it.

### Solution 1: Deploy Ollama to Cloud (Advanced)
- Use Docker to containerize Ollama
- Deploy alongside your app
- More complex setup

### Solution 2: Use Cloud LLM API (Recommended)
Replace Ollama with:
- **OpenAI API** (ChatGPT)
- **Hugging Face API**
- **Google Vertex AI**
- **Claude API**

Example with OpenAI:

```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

---

## Quick Deployment Checklist

### For Streamlit Cloud (Easiest)
- [ ] Create GitHub account
- [ ] Push code to GitHub
- [ ] Connect to Streamlit Cloud
- [ ] Get public link
- [ ] Share with anyone

### For Production
- [ ] Set up environment variables
- [ ] Configure Ollama/LLM API
- [ ] Set up custom domain
- [ ] Enable HTTPS
- [ ] Set up monitoring

---

## Environment Variables

Create `.streamlit/secrets.toml`:

```toml
ollama_host = "http://localhost:11434"
openai_api_key = "sk-..."
database_path = "data/provon_db.pkl"
```

Access in code:

```python
import streamlit as st
api_key = st.secrets["openai_api_key"]
```

---

## Recommended Deployment Path

1. **Quick Test**: Streamlit Cloud (free, easy)
2. **Production**: Google Cloud Run + OpenAI API
3. **Enterprise**: AWS + Ollama Docker + Custom Domain

---

## Support

- Streamlit Docs: https://docs.streamlit.io
- Heroku Docs: https://devcenter.heroku.com
- Google Cloud: https://cloud.google.com/docs
- AWS: https://docs.aws.amazon.com

---

**Your Provon app will be live and accessible from anywhere!** 🚀
