import PySimpleGUI as sg
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

def initialize_agent_components():
    llm = OllamaLLM(
        model="qwen2.5-coder:32b",
        base_url="http://host.docker.internal:11434"
    )
    search = SearxSearchWrapper(searx_host="http://searxng:8080")
    tools = [
        Tool(
            name="Web Search",
            func=search.run,
            description="Useful for searching the internet for current information."
        )
    ]
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

def create_window():
    sg.theme('LightGrey1')
    layout = [
        [sg.Text("Qwen AI Assistant", font=('Helvetica', 20))],
        [sg.Multiline(size=(60, 10), key='-INPUT-', placeholder_text='Enter your question here...')],
        [sg.Button('Ask', bind_return_key=True), sg.Button('Clear'), sg.Button('Exit')],
        [sg.Multiline(size=(60, 15), key='-OUTPUT-', disabled=True)]
    ]
    return sg.Window('Qwen AI Assistant', layout, finalize=True)

def main():
    agent = initialize_agent_components()
    window = create_window()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Clear':
            window['-INPUT-'].update('')
            window['-OUTPUT-'].update('')
        elif event == 'Ask' and values['-INPUT-'].strip():
            query = values['-INPUT-'].strip()
            window['-OUTPUT-'].update('Processing...')
            try:
                response = agent.invoke(query)
                window['-OUTPUT-'].update(response['output'])
            except Exception as e:
                window['-OUTPUT-'].update(f"Error: {str(e)}")

    window.close()

if __name__ == '__main__':
    main()
