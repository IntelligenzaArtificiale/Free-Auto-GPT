from langchain.agents import initialize_agent
from langchain.utilities import PythonREPL
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools.human.tool import HumanInputRun
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API

from langchain.agents import initialize_agent, Tool

import os

#### LOG IN FOR CHATGPT FREE LLM
from dotenv import load_dotenv
load_dotenv()

select_model = input("Select the model you want to use (1 or 2) \n \
1) ChatGPT \n \
2) HuggingChat \n \
>>> ")

if select_model == "1":
    CG_TOKEN = os.getenv("CHATGPT_TOKEN", "your-chatgpt-token")

    if (CG_TOKEN != "your-chatgpt-token"):
        os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    else:
        raise ValueError("ChatGPT Token EMPTY. Edit the .env file and put your ChatGPT token")

    start_chat = os.getenv("USE_EXISTING_CHAT", False)
    if start_chat:
        chat_id = os.getenv("CHAT_ID")
        if chat_id == None:
            raise ValueError("You have to set up your chat-id in the .env file")
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
elif select_model == "2":
    llm=HuggingChatAPI.HuggingChat() 


####

wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPL()
search = DuckDuckGoSearchTool()


#from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain, BaseCombineDocumentsChain
#from Tool import browserQA
#query_website_tool = browserQA.WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))



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
"""

queryWebsite_tool = Tool(
    name= query_website_tool.name,
    func= query_website_tool.run,
    description= query_website_tool.description
)

"""
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
#tools.append(queryWebsite_tool)
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



print(">> START CUSTOM AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt != "exit":
    zero_shot_agent.run(prompt)
    prompt = input("(Enter your task or question) >> ")