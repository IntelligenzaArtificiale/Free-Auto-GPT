from langchain.agents import create_csv_agent
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API

from langchain.utilities import PythonREPL
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

path_csv = input("Enter the path of the csv file: ")

agent = create_csv_agent(llm=llm, tool=PythonREPL(), path=path_csv, verbose=True)

#todo : ADD MEMORY


print(">> START CSV AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt != "exit":
    agent.run(prompt)
    prompt = input("(Enter your task or question) >> ")

