import logging
import os

# Configuration
OLLAMA_BASE_URL = "http://host.docker.internal:11434"
SEARXNG_BASE_URL = "http://searxng:8080"
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8081

# Ensure the logs directory exists
os.makedirs("/app/logs", exist_ok=True)

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    handlers=[
                        logging.FileHandler("/app/logs/app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)