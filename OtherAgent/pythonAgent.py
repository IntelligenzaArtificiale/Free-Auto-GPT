from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API

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

    start_chat = input("Do you want start a chat from existing chat? (y/n): ") # ask if you want start a chat from existing chat
    if start_chat == "y":
        chat_id = input("Insert chat-id (chat.openai.com/c/(IS THIS ->)58XXXX0f-XXXX-XXXX-XXXX-faXXXXd2b50f)  ->") # ask the chat id
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
elif select_model == "2":
    llm=HuggingChatAPI.HuggingChat() 
####



agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

#todo : ADD MEMORY

print(">> STRAT Python AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt != "exit":
    agent_executor.run(prompt)
    prompt = input("(Enter your task or question) >> ")