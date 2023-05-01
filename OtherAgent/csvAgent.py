from langchain.agents import create_csv_agent
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
from langchain.utilities import PythonREPL
import os

#### LOG IN FOR CHATGPT FREE LLM
try :
    #read from args the hf token and chatgpt token 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--chatgpt_token", help="Chatgpt token : \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cookie Value field.")
    args = parser.parse_args()

    if args.chatgpt_token is None:
        raise Exception("You must provide the huggingface token and chatgpt token")

    os.environ["CHATGPT_TOKEN"] = args.chatgpt_token
except:
    print("You must provide the chatgpt token")
    print("chatgpt token: \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cookie Value field.")
    CG_TOKEN = input("Insert chatgpt token >>> ")
    os.environ["CHATGPT_TOKEN"] = CG_TOKEN

llm = ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
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

