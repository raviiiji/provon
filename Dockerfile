FROM ollama/ollama:latest

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the API port
EXPOSE 11434

# Set environment to allow external connections
ENV OLLAMA_HOST=0.0.0.0:11434

# Start with entrypoint script
ENTRYPOINT ["/entrypoint.sh"]