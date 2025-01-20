from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from config import OLLAMA_BASE_URL, SEARXNG_BASE_URL
from model_initialization import available_models
from config import logger

llm = OllamaLLM(
    model=available_models[0],
    base_url=OLLAMA_BASE_URL
)

logger.info(f"Using model: {llm.model}")

searx_search = SearxSearchWrapper(searx_host=SEARXNG_BASE_URL)
duckduckgo_search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="DuckDuckGo Search",
        func=duckduckgo_search.run,
        description="Useful for searching the internet for current information using DuckDuckGo."
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)