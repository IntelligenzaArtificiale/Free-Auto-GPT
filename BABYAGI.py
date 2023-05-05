import os
from dotenv import load_dotenv
from collections import deque
from typing import Dict, List, Optional, Any
from langchain.vectorstores import FAISS
from langchain import HuggingFaceHub
from langchain.docstore import InMemoryDocstore
from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 
from FreeLLM import BingChatAPI # FREE BINGCHAT API
from FreeLLM import BardChatAPI # FREE GOOGLE BARD API
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI
from BabyAgi import BabyAGIMod

import faiss

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

    
    

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "your-huggingface-token")

if (HF_TOKEN != "your-huggingface-token"):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
else:
    raise ValueError("HuggingFace Token EMPTY. Edit the .env file and put your HuggingFace token")



from Embedding import HuggingFaceEmbedding # EMBEDDING FUNCTION

# Define your embedding model
embeddings_model = HuggingFaceEmbedding.newEmbeddingFunction

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})

print(vectorstore)

#DEFINE TOOL
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, LLMChain
from langchain.tools import BaseTool, DuckDuckGoSearchRun


todo_prompt = PromptTemplate.from_template(
    "I need to create a plan for complete me GOAl. Can you help me to create a TODO list? Create only the todo list for this objective: '{objective}'."
)
todo_chain = LLMChain(llm=llm, prompt=todo_prompt)
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]


prefix = """Can you help me to performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
suffix = """Question: {task}. 
{agent_scratchpad}"""
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["objective", "task", "context", "agent_scratchpad"],
)

llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

# START

# Logging of LLMChains
verbose = True

int_max_iterations = input("Enter the maximum number of iterations: (Suggest from 3 and 5) ")
max_iterations = int(int_max_iterations)

# If None, will keep on going forever
max_iterations: Optional[int] =   max_iterations
baby_agi = BabyAGIMod.BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, task_execution_chain=agent_executor, verbose=verbose, max_iterations=max_iterations
)


# DEFINE THE OBJECTIVE - MODIFY THIS
OBJECTIVE = input("Enter the objective of the AI system: (Be realistic!) ")


baby_agi({"objective": OBJECTIVE})
