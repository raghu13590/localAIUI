import sys
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Ollama with Qwen2.5-Coder-32B
llm = OllamaLLM(
    model="qwen2.5-coder:32b",
    base_url="http://host.docker.internal:11434"
)

# Initialize SearxNG with the container name
search = SearxSearchWrapper(searx_host="http://searxng:8080")

# Create a tool for web search
tools = [
    Tool(
        name="Web Search",
        func=search.run,
        description="Useful for when you need to search the internet for current information."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    try:
        response = agent.invoke(question)
        return jsonify({'response': response['output']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_without_flask():
    query = input("Enter your question: ")
    try:
        response = agent.invoke(query)
        print(response)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        run_without_flask()
    else:
        app.run(host='0.0.0.0', port=8081)