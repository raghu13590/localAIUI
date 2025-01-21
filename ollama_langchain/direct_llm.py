import requests
import json
from config import OLLAMA_BASE_URL, logger

def query_llm_directly(question: str, model: str) -> str:
    try:
        logger.debug(f"Querying LLM directly with prompt: {question} and model: {model}")
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={"model": model, "messages": [{"role": "user", "content": question}]}
        )
        response.raise_for_status()

        # Log the raw response content for debugging
        logger.debug(f"Raw response content: {response.content}")

        # Parse the response line by line
        outputs = []
        for line in response.iter_lines():
            if line:
                result = line.decode('utf-8')
                json_result = json.loads(result)
                if 'message' in json_result and 'content' in json_result['message']:
                    outputs.append(json_result['message']['content'])

        final_output = ''.join(outputs)
        logger.debug(f"Direct LLM response: {final_output}")
        return final_output
    except requests.RequestException as e:
        logger.error(f"Error querying LLM directly: {e}")
        return f"Error: {e}"
    except ValueError as e:
        logger.error(f"Error parsing JSON response: {e}")
        return f"Error: {e}"