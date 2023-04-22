import os
from collections import deque
from typing import Dict, List, Optional, Any

from langchain import LLMChain, PromptTemplate

#from t3nsorAPI import gpt3NoInternet  #not working the best
#from quoraAPI import GPT4QUORA        #not working  
#from phindAPI import phindGPT4Internet #not working
#from writesonicAPI import writesonicGPT3Internet #not working


#from youAPI import youGPT3Internet
from sqlchatAPI import sqlchatGPT3  

#from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI

from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

# Define your embedding model
import requests
from retry import retry
import numpy as np

#embeddings_model = OpenAIEmbeddings()

import argparse

parser = argparse.ArgumentParser(description='Script description')

parser.add_argument('--goal', type=str, help='The goal of babyAGI (e.g., learn to play chess)')
parser.add_argument('--token', type=str, help='Your HuggingFace API token, required to use some of the models')
parser.add_argument('--iterations', type=str, help='The number of iterations, if None, will keep on going forever')

args = parser.parse_args()

if args.goal is None or args.token is None or args.iterations is None:
    parser.print_help()
    exit(1)




model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = args.token

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

embedding_size = 1536


def reshape_array(arr):
    # create an array of zeros with shape (1536)
    new_arr = np.zeros((1536,))
    # copy the original array into the new array
    new_arr[:arr.shape[0]] = arr
    # return the new array
    return new_arr

@retry(tries=3, delay=10)
def newEmbeddings(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    result = response.json()
    if isinstance(result, list):
      return result
    elif list(result.keys())[0] == "error":
      raise RuntimeError(
          "The model is currently loading, please re-run the query."
          )
      
def newEmbeddingFunction(texts):
    embeddings = newEmbeddings(texts)
    embeddings = np.array(embeddings, dtype=np.float32)
    shaped_embeddings = reshape_array(embeddings)
    return shaped_embeddings
      
      
# Define your embedding model
embeddings_model = newEmbeddingFunction

# Initialize the vectorstore as empty
import faiss

index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})




#set up the llm API
llm = sqlchatGPT3()


# START

# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = (int)(args.iterations)
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)


# DEFINE THE OBJECTIVE - MODIFY THIS
OBJECTIVE = args.goal


baby_agi({"objective": OBJECTIVE})