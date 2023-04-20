import os
from collections import deque
from typing import Dict, List, Optional, Any

import os
from collections import deque
from typing import Dict, List, Optional, Any

from langchain import LLMChain, PromptTemplate

#from t3nsorAPI import gpt3NoInternet  not working the best
#from quoraAPI import GPT4QUORA        not working
from sqlchatAPI import sqlchatGPT3    #work but low result
#from phindAPI import phindGPT4Internet
#from writesonicAPI import writesonicGPT3Internet
#from youAPI import youGPT3Internet


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

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"

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
max_iterations: Optional[int] = 3
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)


# DEFINE THE OBJECTIVE - MODIFY THIS
OBJECTIVE = "Find best street in Rome for buy an house as an investment."


baby_agi({"objective": OBJECTIVE})