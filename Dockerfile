FROM ollama/ollama:latest

# Create init script to pull tinyllama on first startup
RUN mkdir -p /app && \
    echo '#!/bin/bash' > /app/init.sh && \
    echo 'ollama serve &' >> /app/init.sh && \
    echo 'sleep 10' >> /app/init.sh && \
    echo 'ollama pull tinyllama' >> /app/init.sh && \
    echo 'wait' >> /app/init.sh && \
    chmod +x /app/init.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start with init script
CMD ["/app/init.sh"]