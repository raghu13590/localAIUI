from flask import Flask, request, jsonify
from flask_cors import CORS
from app.core.logging import logger
from app.services.model_service import get_available_models
from app.services.agent_service import create_agent
from app.services.llm_service import query_llm_directly
from langchain_core.messages import HumanMessage

app = Flask(__name__)
CORS(app)

@app.route('/models', methods=['GET'])
def models():
    logger.debug("Received request for models")
    return jsonify({'models': get_available_models()})

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    model_name = data.get('model')

    logger.debug(f"Querying Ollama Agent with prompt: {question} using model: {model_name}")

    try:
        current_agent = create_agent(model_name)
        response = current_agent.invoke([HumanMessage(content=question)])
        logger.debug(f"Ollama agent response: {response}")

        if 'output' in response:
            return jsonify({'response': response['output']})
        else:
            logger.error("No 'output' key in ollama agent response")
            return jsonify({'error': 'Invalid ollama agent response'}), 500

    except Exception as e:
        logger.error(f"Error during ollama agent invocation: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/direct_query', methods=['POST'])
def direct_query():
    data = request.json
    question = data.get('question')
    model_name = data.get('model')

    logger.debug(f"Received direct query: {question} using model: {model_name}")

    try:
        response = query_llm_directly(question, model_name)
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error during direct LLM query: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500 