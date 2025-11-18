FROM ollama/ollama:latest

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start Ollama and pull tinyllama
CMD sh -c "ollama serve & sleep 30 && ollama pull tinyllama && wait"