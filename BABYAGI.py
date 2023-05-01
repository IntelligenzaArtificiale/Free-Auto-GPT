import os
from collections import deque
from typing import Dict, List, Optional, Any
from langchain.vectorstores import FAISS
from langchain import HuggingFaceHub
from langchain.docstore import InMemoryDocstore
from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI
import faiss

select_model = input("Select the model you want to use (1 or 2) \n \
1) ChatGPT \n \
2) HuggingChat \n \
>>> ")

if select_model == "1":
    print("Chatgpt token : \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cooki2e Value field.")
    CG_TOKEN = input("Insert chatgpt token >>> ")
    os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    start_chat = input("Do you want start a chat from existing chat? (y/n): ") # ask if you want start a chat from existing chat
    if start_chat == "y":
        chat_id = input("Insert chat-id (chat.openai.com/c/(IS THIS ->)58XXXX0f-XXXX-XXXX-XXXX-faXXXXd2b50f)  ->") # ask the chat id
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
elif select_model == "2":
    llm=HuggingChatAPI.HuggingChat() 
    
    

print("You must provide the huggingface token and chatgpt token")
print("Huggingface token, check https://huggingface.co/settings/tokens for get your token")
HF_TOKEN = input("Insert huggingface token >>> ")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN



from Embedding import HuggingFaceEmbedding # EMBEDDING FUNCTION

# Define your embedding model
embeddings_model = HuggingFaceEmbedding.newEmbeddingFunction

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})

print(vectorstore)


# START

# Logging of LLMChains
verbose = False

int_max_iterations = input("Enter the maximum number of iterations: (Suggest from 3 and 5) ")
max_iterations = int(int_max_iterations)

# If None, will keep on going forever
max_iterations: Optional[int] =   max_iterations
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)


# DEFINE THE OBJECTIVE - MODIFY THIS
OBJECTIVE = input("Enter the objective of the AI system: (Be realistic!) ")


baby_agi({"objective": OBJECTIVE})