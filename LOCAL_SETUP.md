# Provon - Local Setup Guide (Windows 11)

## Why Streamlit Cloud Doesn't Work

Streamlit Cloud is a **remote server**. Your Ollama runs **locally on your Windows machine**. They can't communicate because:
- Streamlit Cloud ≠ Your Windows machine
- Ollama on localhost:11434 is only accessible from your Windows machine
- Cloud servers can't reach your local services

## Solution: Run Streamlit Locally

### Step 1: Install Ollama (if not already installed)
1. Download from: https://ollama.ai
2. Install and run Ollama
3. In PowerShell, verify it's running:
   ```powershell
   ollama list
   ```

### Step 2: Pull the llama2b Model
```powershell
ollama pull llama2b
```

### Step 3: Start Ollama Service
```powershell
ollama serve
```
Keep this terminal open. Ollama will run on `http://localhost:11434`

### Step 4: Install Python Dependencies (in a new terminal)
```powershell
cd c:\Users\ravir\Desktop\my-notebooklm
pip install -r requirements.txt
```

### Step 5: Run Streamlit Locally
```powershell
streamlit run app.py
```

This will open the app at `http://localhost:8501`

## How It Works Locally

1. **Ollama** runs on your Windows machine (localhost:11434)
2. **Streamlit** runs on your Windows machine (localhost:8501)
3. Both can communicate because they're on the same machine
4. You can upload PDFs, ask questions, and get responses from llama2b

## For Cloud Deployment (Future)

To deploy to Streamlit Cloud, you'd need to:
1. Host Ollama on a cloud server (AWS, Google Cloud, etc.)
2. Update the Ollama URL in `rag_system.py` to point to the cloud server
3. Then deploy to Streamlit Cloud

## Troubleshooting

**Error: "Ollama not running"**
- Make sure you ran `ollama serve` in a terminal
- Check that Ollama is accessible: `curl http://localhost:11434/api/tags`

**Error: "Model not found"**
- Run: `ollama pull llama2b`

**Slow responses**
- llama2b is a 7B parameter model, responses take 10-30 seconds
- This is normal on local machines
