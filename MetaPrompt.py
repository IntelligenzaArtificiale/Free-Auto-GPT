import json
from dotenv import load_dotenv
from pathlib import Path
from json import JSONDecodeError
from langchain import LLMChain, PromptTemplate
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 
from FreeLLM import HuggingChatAPI # FREE HUGGINGCHAT API
from FreeLLM import BingChatAPI # FREE BINGCHAT API
from FreeLLM import BardChatAPI # FREE GOOGLE BARD API

from langchain.memory import ConversationBufferWindowMemory
import os

load_dotenv()

#### LOG IN FOR CHATGPT FREE LLM
select_model = input("Select the model you want to use (1, 2, 3 or 4) \n \
1) ChatGPT \n \
2) HuggingChat \n \
3) BingChat \n \
4) Google Bard \n \
>>> ")

if select_model == "1":
    CG_TOKEN = os.getenv("CHATGPT_TOKEN", "your-chatgpt-token")

    if (CG_TOKEN != "your-chatgpt-token"):
        os.environ["CHATGPT_TOKEN"] = CG_TOKEN
    else:
        raise ValueError("ChatGPT Token EMPTY. Edit the .env file and put your ChatGPT token")

    start_chat = os.getenv("USE_EXISTING_CHAT", False)
    if os.getenv("USE_GPT4") == "True":
        model = "gpt4"
    else:
        model = "default"
        
    if start_chat:
        chat_id = os.getenv("CHAT_ID")
        if chat_id == None:
            raise ValueError("You have to set up your chat-id in the .env file")
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], conversation=chat_id , model=model)
    else:
        llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"], model=model)
              
elif select_model == "2":
    llm=HuggingChatAPI.HuggingChat()

elif select_model == "3":
    if not os.path.exists("cookiesBing.json"):
        raise ValueError("File 'cookiesBing.json' not found! Create it and put your cookies in there in the JSON format.")
    cookie_path = Path() / "cookiesBing.json"
    with open("cookiesBing.json", 'r') as file:
        try:
            file_json = json.loads(file.read())
        except JSONDecodeError:
            raise ValueError("You did not put your cookies inside 'cookiesBing.json'! You can find the simple guide to get the cookie file here: https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required.")
    llm=BingChatAPI.BingChat(cookiepath=str(cookie_path), conversation_style="creative")

elif select_model == "4":
    GB_TOKEN = os.getenv("BARDCHAT_TOKEN", "your-googlebard-token")
    
    if GB_TOKEN != "your-googlebard-token":
        os.environ["BARDCHAT_TOKEN"] = GB_TOKEN
    else:
        raise ValueError("GoogleBard Token EMPTY. Edit the .env file and put your GoogleBard token")
    cookie_path = os.environ["BARDCHAT_TOKEN"]
    llm=BardChatAPI.BardChat(cookie=cookie_path)
    

####


def initialize_chain(instructions, memory=None):
    if memory is None:
        memory = ConversationBufferWindowMemory()
        memory.ai_prefix = "Assistant"

    template = f"""
    Instructions: {instructions}
    {{{memory.memory_key}}}
    Human: {{human_input}}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=template
    )

    chain = LLMChain(
        llm=llm, 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(),
    )
    return chain
    
def initialize_meta_chain():
    meta_template="""
    Assistant has just had the below interactions with a User. Assistant followed their "Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.

    ####

    {chat_history}

    ####

    Please reflect on these interactions.

    You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".

    You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
    """

    meta_prompt = PromptTemplate(
        input_variables=["chat_history"], 
        template=meta_template
    )

    meta_chain = LLMChain(
        llm=llm, 
        prompt=meta_prompt, 
        verbose=True, 
    )
    return meta_chain
    
def get_chat_history(chain_memory):
    memory_key = chain_memory.memory_key
    chat_history = chain_memory.load_memory_variables(memory_key)[memory_key]
    return chat_history

def get_new_instructions(meta_output):
    delimiter = 'Instructions: '
    new_instructions = meta_output[meta_output.find(delimiter)+len(delimiter):]
    return new_instructions

def main(task, max_iters=3, max_meta_iters=5):
    failed_phrase = 'task failed'
    success_phrase = 'task succeeded'
    key_phrases = [success_phrase, failed_phrase]
    
    instructions = 'None'
    for i in range(max_meta_iters):
        print(f'[Episode {i+1}/{max_meta_iters}]')
        chain = initialize_chain(instructions, memory=None)
        output = chain.predict(human_input=task)
        for j in range(max_iters):
            print(f'(Step {j+1}/{max_iters})')
            print(f'Assistant: {output}')
            print(f'Human: ')
            human_input = input()
            if any(phrase in human_input.lower() for phrase in key_phrases):
                break
            output = chain.predict(human_input=human_input)
        if success_phrase in human_input.lower():
            print(f'You succeeded! Thanks for playing!')
            return
        meta_chain = initialize_meta_chain()
        meta_output = meta_chain.predict(chat_history=get_chat_history(chain.memory))
        print(f'Feedback: {meta_output}')
        instructions = get_new_instructions(meta_output)
        print(f'New Instructions: {instructions}')
        print('\n'+'#'*80+'\n')
    print(f'You failed! Thanks for playing!')
    
    

task = input("Enter the objective of the AI system: (Be realistic!) ")
max_iters = int(input("Enter the maximum number of interactions per episode: "))
max_meta_iters = int(input("Enter the maximum number of episodes: "))
main(task, max_iters, max_meta_iters)
