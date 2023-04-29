from langchain import LLMChain, PromptTemplate
from FreeLLM import ChatGPTAPI # FREE CHATGPT API 
from langchain.memory import ConversationBufferWindowMemory
import os


#### LOG IN FOR CHATGPT FREE LLM
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--chatgpt_token", help="chatgpt token, check https://chat.openai.com/api/auth/session for get your token")
args = parser.parse_args()

if args.chatgpt_token is None:
    raise Exception("You must provide the huggingface token and chatgpt token")

os.environ["CHATGPT_TOKEN"] = args.chatgpt_token

llm= ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"])
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