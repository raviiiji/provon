FROM ollama/ollama:latest

# Pull the model
RUN ollama pull llama2b

# Expose the port
EXPOSE 11434

# Start Ollama
CMD ["ollama", "serve"]
