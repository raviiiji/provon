FROM ollama/ollama:latest

# Create startup script
RUN mkdir -p /app && \
    echo '#!/bin/bash' > /app/start.sh && \
    echo 'ollama serve &' >> /app/start.sh && \
    echo 'sleep 15' >> /app/start.sh && \
    echo 'ollama pull neural-chat' >> /app/start.sh && \
    echo 'wait' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start with the script
ENTRYPOINT ["/app/start.sh"]
