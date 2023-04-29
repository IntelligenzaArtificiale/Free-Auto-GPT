from langchain.agents import create_csv_agent
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from langchain.utilities import PythonREPL
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


path_csv = input("Enter the path of the csv file: ")

agent = create_csv_agent(llm=llm, tool=PythonREPL(), path=path_csv, verbose=True)

#todo : ADD MEMORY


print(">> STRAT CSV AGENT")
print("> Digit 'exit' for exit or 'your task or question' for start\n\n")
prompt = input("(Enter your task or question) >> ")
while prompt.toLowerCase() != "exit":
    agent.run(prompt)
    prompt = input("(Enter your task or question) >> ")

