import requests
from app.core.config import OLLAMA_BASE_URL
from app.core.logging import logger
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
        raise RuntimeError(f"Failed to fetch models: {e}") 