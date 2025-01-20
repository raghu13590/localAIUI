import sys
import requests
from config import logger, OLLAMA_BASE_URL
from typing import List

def get_available_models() -> List[str]:
    try:
        logger.debug("Attempting to fetch models from Ollama...")
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags')
        response.raise_for_status()
        models = response.json()
        logger.debug(f"Successfully fetched models: {models}")
        return [model['name'] for model in models['models']]
    except requests.RequestException as e:
        logger.error(f"Error fetching models: {e}")
        return []

available_models = get_available_models()
if not available_models:
    logger.error("No models found on the machine. Exiting...")
    sys.exit("No models found on the machine. Exiting...")