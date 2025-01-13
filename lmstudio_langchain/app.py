import sys
from flask import Flask, request, jsonify
from langchain_openai import OpenAI  # Updated import
from langchain_core.messages import HumanMessage

app = Flask(__name__)

# Initialize LLM with LMStudio configuration
llm = OpenAI(
    base_url="http://host.docker.internal:1234/v1",  # LMStudio API endpoint
    model_name="lmstudio-model",
    openai_api_key="not-needed"  # no API key needed for local models
)

@app.route('/query', methods=['POST'])
def query_llm():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Query the LLM
    response = llm.invoke(prompt)
    return jsonify({"response": response})

def run_without_flask():
    prompt = input("Enter your prompt: ")
    if not prompt:
        print("Prompt is required")
        return

    # Query the LLM
    response = llm.invoke([HumanMessage(content=prompt)])
    print(response)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        run_without_flask()
    else:
        app.run(host='0.0.0.0', port=8082)