import os

# API Configuration
OLLAMA_BASE_URL = "http://host.docker.internal:11434"

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8081

# Paths
LOGS_DIR = "/app/logs"
os.makedirs(LOGS_DIR, exist_ok=True) 