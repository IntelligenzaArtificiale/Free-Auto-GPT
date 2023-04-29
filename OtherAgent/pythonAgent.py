from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
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



agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

agent_executor.run("""Understand, write a single neuron neural network in PyTorch.
Take synthetic data for y=2x. Train for 1000 epochs and print every 100 epochs.
Return prediction for x = 5""")