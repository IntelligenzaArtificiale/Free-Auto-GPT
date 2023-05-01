import os
from collections import deque
from typing import Dict, List, Optional, Any
from langchain.vectorstores import FAISS
from langchain import HuggingFaceHub
from langchain.docstore import InMemoryDocstore
from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI
import faiss

try :
    #read from args the hf token and chatgpt token 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf_token", help="huggingface token, check https://huggingface.co/settings/tokens for get your token")
    parser.add_argument("--chatgpt_token", help="chatgpt token, check https://chat.openai.com/api/auth/session for get your token")
    args = parser.parse_args()

    if args.hf_token is None or args.chatgpt_token is None:
        raise Exception("You must provide the huggingface token and chatgpt token")

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = args.hf_token
    os.environ["CHATGPT_TOKEN"] = args.chatgpt_token
except:
    print("You must provide the huggingface token and chatgpt token")
    print("Huggingface token, check https://huggingface.co/settings/tokens for get your token")
    HF_TOKEN = input("Insert huggingface token >>> ")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
    print("Chatgpt token, check https://chat.openai.com/api/auth/session for get your token")
    CG_TOKEN = input("Insert chatgpt token >>> ")
    os.environ["CHATGPT_TOKEN"] = CG_TOKEN


from Embedding import HuggingFaceEmbedding # EMBEDDING FUNCTION

# Define your embedding model
embeddings_model = HuggingFaceEmbedding.newEmbeddingFunction

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})

print(vectorstore)


llm = ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])

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