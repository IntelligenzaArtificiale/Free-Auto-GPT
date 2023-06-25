# !pip install bs4
# !pip install nest_asyncio

# General
import os
import json
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from json import JSONDecodeError
from langchain.experimental.autonomous_agents.autogpt.agent import AutoGPT
from FreeLLM import ChatGPTAPI  # FREE CHATGPT API
from FreeLLM import HuggingChatAPI  # FREE HUGGINGCHAT API
from FreeLLM import BingChatAPI  # FREE BINGCHAT API
from FreeLLM import BardChatAPI  # FREE GOOGLE BARD API
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.docstore.document import Document
import asyncio
import nest_asyncio


# Needed synce jupyter runs an async eventloop
nest_asyncio.apply()
# [Optional] Set the environment variable Tokenizers_PARALLELISM to false to get rid of the warning
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()
select_model = input(
    "Select the model you want to use (1, 2, 3 or 4) \n \
1) ChatGPT \n \
2) HuggingChat \n \
3) BingChat \n \
4) Google Bard \n \
>>> "
)

if select_model == "1":
    CG_TOKEN = os.getenv("CHATGPT_TOKEN", "your-chatgpt-token")

    if CG_TOKEN != "your-chatgpt-token":
        os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    else:
        raise ValueError(
            "ChatGPT Token EMPTY. Edit the .env file and put your ChatGPT token"
        )

    start_chat = os.getenv("USE_EXISTING_CHAT", False)
    if os.getenv("USE_GPT4") == "True":
        model = "gpt-4"
    else:
        model = "default"

    llm = ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], model=model)

elif select_model == "2":
    emailHF = os.getenv("emailHF", "your-emailHF")
    pswHF = os.getenv("pswHF", "your-pswHF")
    if emailHF != "your-emailHF" or pswHF != "your-pswHF":
        os.environ["emailHF"] = emailHF
        os.environ["pswHF"] = pswHF
    else:
        raise ValueError(
            "HuggingChat Token EMPTY. Edit the .env file and put your HuggingChat credentials"
        )
    
    llm = HuggingChatAPI.HuggingChat(email=os.environ["emailHF"], psw=os.environ["pswHF"])

elif select_model == "3":
    if not os.path.exists("cookiesBing.json"):
        raise ValueError(
            "File 'cookiesBing.json' not found! Create it and put your cookies in there in the JSON format."
        )
    cookie_path = Path() / "cookiesBing.json"
    with open("cookiesBing.json", "r") as file:
        try:
            file_json = json.loads(file.read())
        except JSONDecodeError:
            raise ValueError(
                "You did not put your cookies inside 'cookiesBing.json'! You can find the simple guide to get the cookie file here: https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required."
            )
    llm = BingChatAPI.BingChat(
        cookiepath=str(cookie_path), conversation_style="creative"
    )

elif select_model == "4":
    GB_TOKEN = os.getenv("BARDCHAT_TOKEN", "your-googlebard-token")

    if GB_TOKEN != "your-googlebard-token":
        os.environ["BARDCHAT_TOKEN"] = GB_TOKEN
    else:
        raise ValueError(
            "GoogleBard Token EMPTY. Edit the .env file and put your GoogleBard token"
        )
    cookie_path = os.environ["BARDCHAT_TOKEN"]
    llm = BardChatAPI.BardChat(cookie=cookie_path)


HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "your-huggingface-token")

if HF_TOKEN != "your-huggingface-token":
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
else:
    raise ValueError(
        "HuggingFace Token EMPTY. Edit the .env file and put your HuggingFace token"
    )

# Tools
import os
from contextlib import contextmanager
from typing import Optional
from langchain.agents import tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from tempfile import TemporaryDirectory

ROOT_DIR = TemporaryDirectory()


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
        print(
            "If you are running this for the first time, you nedd to install playwright"
        )
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
from langchain.chains.qa_with_sources.loading import (
    load_qa_with_sources_chain,
    BaseCombineDocumentsChain,
)


def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )


class WebpageQATool(BaseTool):
    name = "query_webpage"
    description = (
        "Browse a webpage and retrieve the information relevant to the question."
    )
    text_splitter: RecursiveCharacterTextSplitter = Field(
        default_factory=_get_text_splitter
    )
    qa_chain: BaseCombineDocumentsChain

    def _run(self, url: str, question: str) -> str:
        """Useful for browsing websites and scraping the text information."""
        result = browse_web_page.run(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        # TODO: Handle this with a MapReduceChain
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i : i + 4]
            window_result = self.qa_chain(
                {"input_documents": input_docs, "question": question},
                return_only_outputs=True,
            )
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [
            Document(page_content="\n".join(results), metadata={"source": url})
        ]
        return self.qa_chain(
            {"input_documents": results_docs, "question": question},
            return_only_outputs=True,
        )

    async def _arun(self, url: str, question: str) -> str:
        raise NotImplementedError


query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))


# Memory
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from Embedding import HuggingFaceEmbedding  # EMBEDDING FUNCTION

from langchain.tools.human.tool import HumanInputRun

# Define your embedding model
embeddings_model = HuggingFaceEmbedding.newEmbeddingFunction
embedding_size = 1536  # if you change this you need to change also in Embedding/HuggingFaceEmbedding.py
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})


# !pip install duckduckgo_search
web_search = DuckDuckGoSearchRun()

tools = [
    web_search,
    WriteFileTool(),
    ReadFileTool(),
    process_csv,
    query_website_tool,
    # HumanInputRun(), # Activate if you want the permit asking for help from the human
]


agent = AutoGPT.from_llm_and_tools(
    ai_name="BingChat",
    ai_role="Assistant",
    tools=tools,
    llm=llm,
    memory=vectorstore.as_retriever(search_kwargs={"k": 5}),
    # human_in_the_loop=True, # Set to True if you want to add feedback at each step.
)
# agent.chain.verbose = True

agent.run([input("Enter the objective of the AI system: (Be realistic!) ")])
