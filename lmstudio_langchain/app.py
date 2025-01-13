from flask import Flask, request, jsonify
from langchain_openai import OpenAI  # Updated import

app = Flask(__name__)

# Initialize LLM with LMStudio configuration
llm = OpenAI(
    base_url="http://localhost:1234/v1",  # Replace with your LMStudio API endpoint
    model_name="local-model",  # Replace with your model name
    openai_api_key="not-needed"  # LMStudio doesn't require an API key
)

@app.route('/query', methods=['POST'])
def query_llm():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Query the LLM
    response = llm(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
