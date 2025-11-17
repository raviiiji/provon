FROM ollama/ollama:latest

# Start ollama in background, pull model, then keep running
RUN mkdir -p /app && \
    echo '#!/bin/bash' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo 'echo "Starting Ollama..."' >> /app/start.sh && \
    echo 'ollama serve &' >> /app/start.sh && \
    echo 'OLLAMA_PID=$!' >> /app/start.sh && \
    echo 'sleep 15' >> /app/start.sh && \
    echo 'echo "Pulling mistral model..."' >> /app/start.sh && \
    echo 'ollama pull mistral' >> /app/start.sh && \
    echo 'echo "Model ready!"' >> /app/start.sh && \
    echo 'wait $OLLAMA_PID' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start with the script
CMD ["/bin/bash", "/app/start.sh"]
