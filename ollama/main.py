import sys
from app.core.config import FLASK_HOST, FLASK_PORT
from app.api.routes import app
from app.services.agent_service import run_cli_mode

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        run_cli_mode()
    else:
        app.run(host=FLASK_HOST, port=FLASK_PORT)

if __name__ == "__main__":
    main() 