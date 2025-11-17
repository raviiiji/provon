FROM ollama/ollama:latest

# Pull a lightweight model (neural-chat is smaller than llama2b)
# neural-chat: ~4GB, faster responses
# If you want llama2b instead, uncomment below and comment out neural-chat
RUN ollama pull neural-chat

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start Ollama service
CMD ["ollama", "serve"]
