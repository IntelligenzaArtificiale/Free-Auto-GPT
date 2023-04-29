from langchain.agents import initialize_agent
from langchain.utilities import PythonREPL
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchTool
from langchain.tools.human.tool import HumanInputRun
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from langchain.agents import initialize_agent, Tool
import os

#### LOG IN FOR CHATGPT FREE LLM
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--chatgpt_token", help="chatgpt token, check https://chat.openai.com/api/auth/session for get your token")
args = parser.parse_args()

if args.chatgpt_token is None:
    raise Exception("You must provide the huggingface token and chatgpt token")

os.environ["CHATGPT_TOKEN"] = args.chatgpt_token

llm = ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
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
while prompt.toLowerCase() != "exit":
    zero_shot_agent.run(prompt)
    prompt = input("(Enter your task or question) >> ")