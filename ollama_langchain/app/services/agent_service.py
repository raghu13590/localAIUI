from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_core.messages import HumanMessage
from app.core.config import OLLAMA_BASE_URL
from app.core.logging import logger

def create_tools():
    duckduckgo_search = DuckDuckGoSearchRun()
    return [
        Tool(
            name="DuckDuckGo Search",
            func=duckduckgo_search.run,
            description="Useful for searching the internet for current information using DuckDuckGo."
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
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

def run_cli_mode():
    from app.services.model_service import get_available_models
    agent = create_agent(get_available_models()[0])
    
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        logger.debug(f"Querying Ollama Agent with prompt: {query}")
        try:
            response = agent.invoke([HumanMessage(content=query)])
            logger.debug(f"Ollama agent response: {response}")
            print(response['output'])
        except Exception as e:
            logger.error(f"Error during ollama agent invocation: {str(e)}", exc_info=True)
            print(f"Error: {e}") 