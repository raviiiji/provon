FROM ollama/ollama:latest

# Create startup script that pulls a smaller model
RUN mkdir -p /app && \
    echo '#!/bin/bash' > /app/start.sh && \
    echo 'ollama serve &' >> /app/start.sh && \
    echo 'sleep 10' >> /app/start.sh && \
    echo 'ollama pull mistral' >> /app/start.sh && \
    echo 'tail -f /dev/null' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start with the script
CMD ["/app/start.sh"]
