import json
from pathlib import Path
from json import JSONDecodeError
from langchain.agents import initialize_agent
from langchain.utilities import PythonREPL
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.tools.human.tool import HumanInputRun
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API
from FreeLLM import BingChatAPI # FREE BINGCHAT API
from FreeLLM import BardChatAPI # FREE Google BArd API
from langchain.agents import initialize_agent, Tool

import os

#### LOG IN FOR CHATGPT FREE LLM
from dotenv import load_dotenv
load_dotenv()
select_model = input("Select the model you want to use (1, 2, 3 or 4) \n \
1) ChatGPT \n \
2) HuggingChat \n \
3) BingChat \n \
4) Google Bard \n \
>>> ")

if select_model == "1":
    CG_TOKEN = os.getenv("CHATGPT_TOKEN", "your-chatgpt-token")

    if (CG_TOKEN != "your-chatgpt-token"):
        os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    else:
        raise ValueError("ChatGPT Token EMPTY. Edit the .env file and put your ChatGPT token")

    start_chat = os.getenv("USE_EXISTING_CHAT", False)
    if os.getenv("USE_GPT4") == "True":
        model = "gpt4"
    else:
        model = "default"
        
    if start_chat:
        chat_id = os.getenv("CHAT_ID")
        if chat_id == None:
            raise ValueError("You have to set up your chat-id in the .env file")
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id , model=model)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], model=model)
              
elif select_model == "2":
    if not os.path.exists("cookiesHuggingChat.json"):
        raise ValueError(
            "File 'cookiesHuggingChat.json' not found! Create it and put your cookies in there in the JSON format."
        )
    cookie_path = Path() / "cookiesHuggingChat.json"
    with open("cookiesHuggingChat.json", "r") as file:
        try:
            file_json = json.loads(file.read())
        except JSONDecodeError:
            raise ValueError(
                "You did not put your cookies inside 'cookiesHuggingChat.json'! You can find the simple guide to get the cookie file here: https://github.com/IntelligenzaArtificiale/Free-Auto-GPT"
            )  
    llm = HuggingChatAPI.HuggingChat(cookiepath = str(cookie_path))

elif select_model == "3":
    if not os.path.exists("cookiesBing.json"):
        raise ValueError("File 'cookiesBing.json' not found! Create it and put your cookies in there in the JSON format.")
    cookie_path = Path() / "cookiesBing.json"
    with open("cookiesBing.json", 'r') as file:
        try:
            file_json = json.loads(file.read())
        except JSONDecodeError:
            raise ValueError("You did not put your cookies inside 'cookiesBing.json'! You can find the simple guide to get the cookie file here: https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required.")
    llm=BingChatAPI.BingChat(cookiepath=str(cookie_path), conversation_style="creative")

elif select_model == "4":
    GB_TOKEN = os.getenv("BARDCHAT_TOKEN", "your-googlebard-token")
    
    if GB_TOKEN != "your-googlebard-token":
        os.environ["BARDCHAT_TOKEN"] = GB_TOKEN
    else:
        raise ValueError("GoogleBard Token EMPTY. Edit the .env file and put your GoogleBard token")
    cookie_path = os.environ["BARDCHAT_TOKEN"]
    llm=BardChatAPI.BardChat(cookie=cookie_path)
    
####

wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPL()
search = DuckDuckGoSearchRun()


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
