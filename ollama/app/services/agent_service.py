from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool, AgentType, create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from app.core.config import OLLAMA_BASE_URL
from app.core.logging import logger

def create_tools():
    duckduckgo_search = DuckDuckGoSearchRun()
    def logged_search(input):
        logger.debug(f"Searching DuckDuckGo with query: {input}")
        result = duckduckgo_search.run(input)
        logger.debug(f"DuckDuckGo search result: {result}")
        return result

    return [
        Tool(
            name="DuckDuckGo Search",
            func=logged_search,  # Changed from lambda to wrapped function
            description="Searches the web for up-to-date information, news, or facts using DuckDuckGo. Use this tool when you need current or real-time data not present in your training or context.",
            handle_tool_error=True
        )
    ]

def create_agent(model_name):
    llm = OllamaLLM(
        model=model_name,
        base_url=OLLAMA_BASE_URL
    )
    
    tools = create_tools()
    
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )

def extract_and_display_thoughts(response, agent):
    thoughts = []

    try:
        # Convert response to string for processing
        response_str = str(response)

        # Method 1: Extract thoughts from response using timestamp pattern
        lines = response_str.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Look for "Thought:" as a clear marker
            if 'Thought:' in line:
                thought = line.split('Thought:')[-1].strip()
                if thought and thought not in thoughts:
                    thoughts.append(thought)
            i += 1

        # Method 2: Look for JSON structures that might contain thoughts
        if not thoughts and '"action": "' in response_str and '"action_input": "' in response_str:
            # Try to extract from action_input if it contains thought content
            import re
            thought_matches = re.findall(r'"action_input":[^"]*"([^"]*Thought:[^"]*)"', response_str)
            for match in thought_matches:
                if 'Thought:' in match:
                    thought = match.split('Thought:')[-1].strip()
                    if thought and thought not in thoughts:
                        thoughts.append(thought)

        # Method 3: Extract from intermediate steps if available
        if not thoughts and isinstance(response, dict) and 'intermediate_steps' in response:
            for step in response['intermediate_steps']:
                if isinstance(step, tuple) and len(step) > 0:
                    action = step[0]
                    if hasattr(action, 'log') and 'Thought:' in action.log:
                        thought = action.log.split('Thought:')[-1].split('\n')[0].strip()
                        thoughts.append(thought)

    except Exception as e:
        logger.error(f"Error extracting thoughts: {str(e)}", exc_info=True)

    return thoughts

def run_cli_mode():
    from app.services.model_service import get_available_models
    available_models = get_available_models()

    if not available_models:
        logger.error("No available models found. Please download a model first.")
        print("Error: No models available. Please install at least one model.")
        return

    agent = create_agent(available_models[0])

    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        logger.debug(f"Querying Ollama Agent with prompt: {query}")
        try:
            response = agent.invoke([HumanMessage(content=query)])
            logger.debug(f"Ollama agent response: {response}")

            # Display reasoning steps
            if 'intermediate_steps' in response:
                print("\n[Reasoning Steps]")
                for i, step in enumerate(response['intermediate_steps'], 1):
                    action = step[0]
                    thought = action.log.split('Thought: ')[-1].split('\n')[0].strip()
                    print(f"Step {i}: {thought}")
                    # Add search query and result display
                    print(f"  Search Query: {action.tool_input}")
                    print(f"  Search Result: {step[1][:200]}...")  # Truncate long responses

            print(f"\n[Final Answer]\n{response['output']}")

            # Extract thoughts using our new function
            thoughts = extract_and_display_thoughts(response, agent)

            if thoughts:
                print("\n[Reasoning Steps]")
                for i, thought in enumerate(thoughts, 1):
                    print(f"Step {i}: {thought}")
            else:
                # Fallback to parsing raw response
                print("\n[Reasoning Steps]")
                raw_response = str(response)
                thought_parts = raw_response.split("Thought:")
                for i, part in enumerate(thought_parts[1:], 1):
                    thought = part.split("\n")[0].strip()
                    print(f"Step {i}: {thought}")

            # Get final answer
            output = response.content if hasattr(response, 'content') else str(response)
            print(f"\n[Final Answer]\n{output}")

        except Exception as e:
            logger.error(f"Error during ollama agent invocation: {str(e)}", exc_info=True)
            print(f"Error: {e}")