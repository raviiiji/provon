FROM ollama/ollama:latest

# Create startup script
WORKDIR /app
RUN echo '#!/bin/sh' > start.sh && \
    echo 'echo "Starting Ollama service..."' >> start.sh && \
    echo 'ollama serve &' >> start.sh && \
    echo 'OLLAMA_PID=$!' >> start.sh && \
    echo 'echo "Waiting for Ollama to initialize..."' >> start.sh && \
    echo 'sleep 30' >> start.sh && \
    echo 'echo "Pulling tinyllama model (this may take 5-10 minutes)..."' >> start.sh && \
    echo 'ollama pull tinyllama' >> start.sh && \
    echo 'echo "Model ready! Keeping service alive..."' >> start.sh && \
    echo 'wait $OLLAMA_PID' >> start.sh && \
    chmod +x start.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Run the startup script
CMD ["/app/start.sh"]