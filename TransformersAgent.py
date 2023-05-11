from hfAgent import agents
from dotenv import load_dotenv

import os
import json

from json import JSONDecodeError
from pathlib import Path

import huggingface_hub

load_dotenv()

select_model = input(
    "Select the model you want to use (1, 2, 3, 4, 5, 6) \n \
1) ChatGPT \n \
2) HuggingChat (NOT GOOD RESULT)\n \
3) BingChat (NOT GOOD RESULT)\n \
4) BardChat \n \
5) StarCoder\n \
6) OpenAssistant\n \
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
        model = "gpt4"
    else:
        model = "default"

    if start_chat:
        chat_id = os.getenv("CHAT_ID")
        if chat_id == None:
            raise ValueError("You have to set up your chat-id in the .env file")
        agent = agents.ChatGPTAgent(
            token=os.environ["CHATGPT_TOKEN"], conversation=chat_id, model=model
        )
    else:
        agent = agents.ChatGPTAgent(token=os.environ["CHATGPT_TOKEN"], model=model)

elif select_model == "2":
    agent = agents.HuggingChatAgent()

elif select_model == "3":
    if not os.path.exists("cookiesBing.json"):
        raise ValueError(
            "File 'cookiesBing.json' not found! Create it and put your cookies in there in the JSON format."
        )
    cookie_path = "cookiesBing.json"
    with open("cookiesBing.json", "r") as file:
        try:
            file_json = json.loads(file.read())
        except JSONDecodeError:
            raise ValueError(
                "You did not put your cookies inside 'cookiesBing.json'! You can find the simple guide to get the cookie file here: https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required."
            )
    agent = agents.BingChatAgent(cookiepath=cookie_path, conversation="balanced")

elif select_model == "4":
    GB_TOKEN = os.getenv("BARDCHAT_TOKEN", "your-googlebard-token")

    if GB_TOKEN != "your-googlebard-token":
        os.environ["BARDCHAT_TOKEN"] = GB_TOKEN
    else:
        raise ValueError(
            "GoogleBard Token EMPTY. Edit the .env file and put your GoogleBard token"
        )
    cookie = os.environ["BARDCHAT_TOKEN"]
    agent = agents.BardChatAgent(token=cookie)
elif select_model == "5":
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "your-huggingface-token")
    if HF_TOKEN != "your-huggingface-token":
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
        huggingface_hub.login(token=HF_TOKEN)
    else:
        raise ValueError(
            "HuggingFace Token EMPTY. Edit the .env file and put your HuggingFace token"
        )

    from transformers.tools import HfAgent

    agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

elif select_model == "6":
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "your-huggingface-token")
    if HF_TOKEN != "your-huggingface-token":
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
        huggingface_hub.login(token=HF_TOKEN)
    else:
        raise ValueError(
            "HuggingFace Token EMPTY. Edit the .env file and put your HuggingFace token"
        )

    from transformers.tools import HfAgent

    agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

    from transformers.tools import HfAgent

    agent = HfAgent(
        url_endpoint="https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
    )


prompt = input(">>> Input prompt:\n>")
while prompt != "exit":
    agent.run(prompt, remote=True)
    prompt = input(">>> Input prompt:\n>")
