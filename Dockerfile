FROM ollama/ollama:latest

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start Ollama service
CMD ["ollama", "serve"]
