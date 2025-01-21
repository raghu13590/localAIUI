import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import logger, FLASK_HOST, FLASK_PORT, OLLAMA_BASE_URL
from agent_initialization import agent, tools
from model_initialization import available_models
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, AgentType
from direct_llm import query_llm_directly

app = Flask(__name__)
CORS(app)

@app.route('/models', methods=['GET'])
def models():
    logger.debug("Received request for models")
    return jsonify({'models': available_models})

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    model_name = data.get('model')

    logger.debug(f"Received query: {question} using model: {model_name}")

    try:
        current_llm = OllamaLLM(
            model=model_name,
            base_url=OLLAMA_BASE_URL
        )

        current_agent = initialize_agent(
            tools,
            current_llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )

        response = current_agent.invoke([HumanMessage(content=question)])
        logger.debug(f"Agent response: {response}")

        if 'output' in response:
            return jsonify({'response': response['output']})
        else:
            logger.error("No 'output' key in agent response")
            return jsonify({'error': 'Invalid response from agent'}), 500

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

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        run_without_flask()
    else:
        app.run(host=FLASK_HOST, port=FLASK_PORT)