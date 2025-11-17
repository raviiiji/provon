#!/bin/bash
set -e

echo "Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to start..."
sleep 15

echo "Pulling tinyllama model..."
ollama pull tinyllama

echo "Model ready!"
wait $OLLAMA_PID
