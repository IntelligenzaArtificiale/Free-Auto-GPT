# !pip install bs4
# !pip install nest_asyncio

# General 
import os
import pandas as pd
from langchain.experimental.autonomous_agents.autogpt.agent import AutoGPT
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 

from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.docstore.document import Document
import asyncio
import nest_asyncio


# Needed synce jupyter runs an async eventloop
nest_asyncio.apply()

try :
    #read from args the hf token and chatgpt token 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf_token", help="huggingface token, check https://huggingface.co/settings/tokens for get your token")
    parser.add_argument("--chatgpt_token", help="chatgpt token: \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cookie Value field.")
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
    print("Chatgpt token : \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cookie Value field.")
    CG_TOKEN = input("Insert chatgpt token >>> ")
    os.environ["CHATGPT_TOKEN"] = CG_TOKEN

start_chat = input("Do you want start a chat from existing chat? (y/n): ") # ask if you want start a chat from existing chat
if start_chat == "y":
    chat_id = input("Insert chat-id (chat.openai.com/c/(IS THIS ->)58XXXX0f-XXXX-XXXX-XXXX-faXXXXd2b50f)  ->") # ask the chat id
    llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id)
else:
    llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])


# Tools
import os
from contextlib import contextmanager
from typing import Optional
from langchain.agents import tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool

ROOT_DIR = "data/"

@contextmanager
def pushd(new_dir):
    """Context manager for changing the current working directory."""
    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)

@tool
def process_csv(
    csv_file_path: str, instructions: str, output_path: Optional[str] = None
) -> str:
    """Process a CSV by with pandas in a limited REPL.\
 Only use this after writing data to disk as a csv file.\
 Any figures must be saved to disk to be viewed by the human.\
 Instructions should be written in natural language, not code. Assume the dataframe is already loaded."""
    with pushd(ROOT_DIR):
        try:
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            return f"Error: {e}"
        agent = create_pandas_dataframe_agent(llm, df, max_iterations=30, verbose=True)
        if output_path is not None:
            instructions += f" Save output to disk at {output_path}"
        try:
            result = agent.run(instructions)
            return result
        except Exception as e:
            return f"Error: {e}"
        
        
# !pip install playwright
# !playwright install
async def async_load_playwright(url: str) -> str:
    """Load the specified URLs using Playwright and parse using BeautifulSoup."""
    from bs4 import BeautifulSoup
    from playwright.async_api import async_playwright
    try:
        print(">>> WARNING <<<")
        print("If you are running this for the first time, you nedd to install playwright")
        print(">>> AUTO INSTALLING PLAYWRIGHT <<<")
        os.system("playwright install")
        print(">>> PLAYWRIGHT INSTALLED <<<")
    except:
        print(">>> PLAYWRIGHT ALREADY INSTALLED <<<")
        pass
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            soup = BeautifulSoup(page_source, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            results = "\n".join(chunk for chunk in chunks if chunk)
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results

def run_async(coro):
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coro)

@tool
def browse_web_page(url: str) -> str:
    """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
    return run_async(async_load_playwright(url))


from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pydantic import Field
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain, BaseCombineDocumentsChain

def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 500,
        chunk_overlap  = 20,
        length_function = len,
    )


class WebpageQATool(BaseTool):
    name = "query_webpage"
    description = "Browse a webpage and retrieve the information relevant to the question."
    text_splitter: RecursiveCharacterTextSplitter = Field(default_factory=_get_text_splitter)
    qa_chain: BaseCombineDocumentsChain
    
    def _run(self, url: str, question: str) -> str:
        """Useful for browsing websites and scraping the text information."""
        result = browse_web_page.run(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        # TODO: Handle this with a MapReduceChain
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i:i+4]
            window_result = self.qa_chain({"input_documents": input_docs, "question": question}, return_only_outputs=True)
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [Document(page_content="\n".join(results), metadata={"source": url})]
        return self.qa_chain({"input_documents": results_docs, "question": question}, return_only_outputs=True)
    
    async def _arun(self, url: str, question: str) -> str:
        raise NotImplementedError
      

query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))


# Memory
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from Embedding import HuggingFaceEmbedding # EMBEDDING FUNCTION

from langchain.tools.human.tool import HumanInputRun

# Define your embedding model
embeddings_model = HuggingFaceEmbedding.newEmbeddingFunction
embedding_size = 1536 # if you change this you need to change also in Embedding/HuggingFaceEmbedding.py
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})


# !pip install duckduckgo_search
web_search = DuckDuckGoSearchRun()

tools = [
    web_search,
    WriteFileTool(root_dir="./data"),
    ReadFileTool(root_dir="./data"),
    process_csv,
    query_website_tool,
    # HumanInputRun(), # Activate if you want the permit asking for help from the human
]


agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=llm,
    memory=vectorstore.as_retriever(search_kwargs={"k": 8}),
    # human_in_the_loop=True, # Set to True if you want to add feedback at each step.
)
# agent.chain.verbose = True

agent.run([input("Enter the objective of the AI system: (Be realistic!) ")])