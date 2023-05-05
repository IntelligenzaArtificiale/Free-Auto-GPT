from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API
from FreeLLM import BingChatAPI # FREE BINGCHAT API
from FreeLLM import BardChatAPI # FREE GOOGLE BARD API

import os

#### LOG IN FOR CHATGPT FREE LLM
from dotenv import load_dotenv
load_dotenv()

select_model = input("Select the model you want to use (1 or 2) \n \
1) ChatGPT \n \
2) HuggingChat \n \
3) BingChat \n \
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
elif select_model == "3":
    if os.environ["BINGCHAT_COOKIEPATH"] == "your-bingchat-cookiepath":
        raise ValueError("BingChat CookiePath EMPTY. Edit the .env file and put your BingChat cookiepath")
    cookie_path = os.environ["BINGCHAT_COOKIEPATH"]
    llm=BingChatAPI.BingChat(cookiepath=cookie_path, conversation_style="creative")
elif select_model == "4":
    if os.environ["BARDCHAT_TOKEN"] == "your-googlebard-cookiepath":
        raise ValueError("GoogleBard CookiePath EMPTY. Edit the .env file and put your GoogleBard cookiepath")
    cookie_path = os.environ["BARDCHAT_TOKEN"]
    llm=BardChatAPI.BardChat(cookie=cookie_path)
####



agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

#todo : ADD MEMORY

print(">> START Python AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt != "exit":
    agent_executor.run(prompt)
    prompt = input("(Enter your task or question) >> ")
