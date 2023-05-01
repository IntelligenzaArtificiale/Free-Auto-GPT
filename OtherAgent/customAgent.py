from langchain.agents import initialize_agent
from langchain.utilities import PythonREPL
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchTool
from langchain.tools.human.tool import HumanInputRun
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API

from langchain.agents import initialize_agent, Tool
import os

#### LOG IN FOR CHATGPT FREE LLM
select_model = input("Select the model you want to use (1 or 2) \n \
1) ChatGPT \n \
2) HuggingChat \n \
>>> ")

if select_model == "1":
    print("Chatgpt token : \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cooki2e Value field.")
    CG_TOKEN = input("Insert chatgpt token >>> ")
    os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    start_chat = input("Do you want start a chat from existing chat? (y/n): ") # ask if you want start a chat from existing chat
    if start_chat == "y":
        chat_id = input("Insert chat-id (chat.openai.com/c/(IS THIS ->)58XXXX0f-XXXX-XXXX-XXXX-faXXXXd2b50f)  ->") # ask the chat id
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
elif select_model == "2":
    llm=HuggingChatAPI.HuggingChat() 

####

wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPL()
search = DuckDuckGoSearchTool()

#define TOOLs

tools = [
    Tool(
        name = "python repl",
        func=python_repl.run,
        description="useful for when you need to use python to answer a question. You should input python code"
    )
]

wikipedia_tool = Tool(
    name='wikipedia',
    func= wikipedia.run,
    description="Useful for when you need to look up a topic, country or person on wikipedia"
)

duckduckgo_tool = Tool(
    name='DuckDuckGo Search',
    func= search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)

#human_input_tool = Tool(
    #name='human input',
    #func= HumanInputRun.run,
    #description="Useful for when you need to ask a human a question. be specific with your input."
#)

#Add here your tools
#custom_tool = Tool(
    #name='custom tool',
    #func= custom_tool.run,
    #description="My fantasitc tool"
#)


tools.append(duckduckgo_tool)
tools.append(wikipedia_tool)
#tools.append(human_input_tool)
#tools.append(custom_tool)


#Create the Agent
iteration = (int(input("Enter the number of iterations: ")) if input("Do you want to set the number of iterations? (y/n): ") == "y" else 3)

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description", 
    tools=tools, 
    llm=llm,
    verbose=True,
    max_iterations=iteration,
)


print(">> STRAT CUSTOM AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt != "exit":
    zero_shot_agent.run(prompt)
    prompt = input("(Enter your task or question) >> ")