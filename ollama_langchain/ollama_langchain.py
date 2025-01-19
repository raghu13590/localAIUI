import sys
import requests
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_core.messages import HumanMessage
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add new function to get models
def get_available_models():
    try:
        logger.debug("Attempting to fetch models from Ollama...")
        response = requests.get('http://host.docker.internal:11434/api/tags')
        if response.status_code == 200:
            models = response.json()
            logger.debug(f"Successfully fetched models: {models}")
            return [model['name'] for model in models['models']]
        logger.warning(f"Failed to fetch models. Status code: {response.status_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return []

# Check for available models during startup
available_models = get_available_models()
if not available_models:
    logger.error("No models found on the machine. Exiting...")
    sys.exit("No models found on the machine. Exiting...")

# Initialize Ollama with the first available model
llm = OllamaLLM(
    model=available_models[0],
    base_url="http://host.docker.internal:11434"
)

# Print the model details to verify
logger.info(f"Using model: {llm.model}")

# Initialize SearxNG with the container name
searx_search = SearxSearchWrapper(searx_host="http://searxng:8080")

# Initialize DuckDuckGo search
duckduckgo_search = DuckDuckGoSearchRun()

# Create a tool for web search
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=duckduckgo_search.run,
        description="Useful for searching the internet for current information using DuckDuckGo."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# Add new endpoint to get models
@app.route('/models', methods=['GET'])
def models():
    logger.debug("Received request for models")
    return jsonify({'models': available_models})

# Update query endpoint to accept model parameter
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    model_name = data.get('model')

    if not model_name:
        return jsonify({'error': 'Model parameter is required'}), 400

    logger.debug(f"Received query: {question} using model: {model_name}")

    # Create a new LLM instance with the selected model
    current_llm = OllamaLLM(
        model=model_name,
        base_url="http://host.docker.internal:11434"
    )

    # Create a new agent with the selected model
    current_agent = initialize_agent(
        tools,
        current_llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    try:
        response = current_agent.invoke([HumanMessage(content=question)])
        logger.debug(f"Agent response: {response}")
        return jsonify({'response': response['output']})
    except Exception as e:
        logger.error(f"Error during agent invocation: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def run_without_flask():
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        logger.debug(f"Received query: {query}")
        try:
            response = agent.invoke([HumanMessage(content=query)])
            logger.debug(f"Agent response: {response}")
            print(response['output'])
        except Exception as e:
            logger.error(f"Error during agent invocation: {str(e)}", exc_info=True)
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        run_without_flask()
    else:
        app.run(host='0.0.0.0', port=8081)