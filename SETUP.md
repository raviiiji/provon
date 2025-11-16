# Provon Setup Guide

## Prerequisites

- Python 3.8+
- Ollama installed and running (`ollama serve`)
- llama2:latest model downloaded in Ollama

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements-advanced.txt
```

### 2. Ensure Ollama is Running

```bash
ollama serve
```

In another terminal, pull the llama2 model:
```bash
ollama pull llama2:latest
```

### 3. Add Your Documents to Backend

```bash
python manage_backend.py
```

Select option 3 to add your documents. They will be stored permanently in `data/provon_db.pkl`.

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## First Run

1. **Backend loads** - Initializes with base knowledge (llama2b)
2. **Welcome message** - Shows greeting from llama2:latest
3. **Ready to query** - Ask questions about your documents or general topics

## Testing

### Test Query 1: General Knowledge
- Query: "What is machine learning?"
- Expected: Answer from base knowledge with "priiii" prefix

### Test Query 2: Your Documents
- Upload a PDF/TXT/DOCX
- Query: Ask something from the document
- Expected: Answer from your document with sources

### Test Query 3: Fallback
- Query: Something not in your documents
- Expected: Fallback answer from base knowledge

## Troubleshooting

### "Connection refused" error
- Make sure Ollama is running: `ollama serve`

### "Model not found" error
- Pull the model: `ollama pull llama2:latest`

### "No documents in knowledge base"
- This is normal on first run
- Use `manage_backend.py` to add documents
- Or upload documents through the app UI

### Slow responses
- First query is slower (model loading)
- Subsequent queries are faster
- For production, consider using a faster model

## Production Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Create new app → Select your repo
4. Set environment variables if needed

### Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile

# Deploy
git push heroku main
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-advanced.txt .
RUN pip install -r requirements-advanced.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

## Configuration

### Change Model
Edit `rag_system.py` line 174:
```python
response = ollama.generate(model='mistral:latest', prompt=prompt)
```

### Change Base Knowledge
Edit `base_knowledge.py` and add/modify chunks in `BASE_KNOWLEDGE_CHUNKS`

### Change Database Location
Edit `backend_db.py` line 6:
```python
def __init__(self, db_path="your/custom/path.pkl"):
```

## Performance Tips

1. **Use faster models** - mistral:latest is faster than llama2
2. **Increase chunk size** - In `document_processor.py`
3. **Use GPU** - Configure Ollama to use GPU
4. **Cache embeddings** - Already done with sentence-transformers

## Next Steps

1. ✅ Install dependencies
2. ✅ Start Ollama
3. ✅ Add documents to backend
4. ✅ Run the app
5. ✅ Test queries
6. ✅ Deploy to production

---

**Ready to go!** Your Provon system is fully set up. 🚀
