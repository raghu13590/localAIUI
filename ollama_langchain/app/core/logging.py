import logging
import os
from .config import LOGS_DIR

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(os.path.join(LOGS_DIR, "app.log")),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger() 