from langchain_ollama import OllamaLLM
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# Initialize Ollama with Qwen2.5-Coder-32B
llm = OllamaLLM(model="qwen2.5-coder:32b")

# Initialize SearxNG
search = SearxSearchWrapper(searx_host="http://localhost:8080")

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

# Example usage
query = input("Enter your question: ")
try:
    response = agent.invoke(query)
    print(response)
except ValueError as e:
    print(f"Error: {e}")