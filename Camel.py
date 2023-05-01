from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)

from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from FreeLLM import ChatGPTAPI # FREE CHATGPT API
import streamlit as st
from streamlit_chat_media import message
import os

st.set_page_config(
    page_title="FREE AUTOGPT 🚀 by Intelligenza Artificiale Italia",
    page_icon="🚀",
    layout="wide",
    menu_items={
        'Get help': 'https://www.intelligenzaartificialeitalia.net/',
        'Report a bug': "mailto:servizi@intelligenzaartificialeitalia.net",
        'About': "# *🚀  FREE AUTOGPT  🚀* "
    }
)


st.markdown("<style> iframe > div {    text-align: left;} </style>", unsafe_allow_html=True)
 

  
class CAMELAgent:

    def __init__(
        self,
        system_message: SystemMessage,
        model: None,
    ) -> None:
        self.system_message = system_message.content
        self.model = model
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]
 
    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        return self.stored_messages

    def step(
        self,
        input_message: HumanMessage,
    ) -> AIMessage:
        messages = self.update_messages(input_message)
        output_message = self.model(str(input_message.content))
        self.update_messages(output_message)
        print(f"AI Assistant:\n\n{output_message}\n\n")
        return output_message

    


col1, col2 = st.columns(2)
assistant_role_name = col1.text_input("Assistant Role Name", "Python Programmer")
user_role_name = col2.text_input("User Role Name", "Stock Trader")
task = st.text_area("Task", "Develop a trading bot for the stock market")
word_limit = st.number_input("Word Limit", 10, 1500, 50)

token_CG = st.text_input("Insert your ChatGPT token", "")
with st.expander("How to get your ChatGPT token"):
    st.markdown("chatgpt token: \n \
    Go to https://chat.openai.com/chat and open the developer tools by F12. \n \
    Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com \n \
    Copy the value in the Cookie Value field.", unsafe_allow_html=True)

if st.button("Start Autonomus AI AGENT") and token_CG != "":
    os.environ["CHATGPT_TOKEN"] = token_CG
    task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
    task_specifier_prompt = (
    """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
    Please make it more specific. Be creative and imaginative.
    Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
    )
    task_specifier_template = HumanMessagePromptTemplate.from_template(template=task_specifier_prompt)
    
    task_specify_agent = CAMELAgent(task_specifier_sys_msg,  ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"]))
    task_specifier_msg = task_specifier_template.format_messages(assistant_role_name=assistant_role_name,
                                                                user_role_name=user_role_name,
                                                                task=task, word_limit=word_limit)[0]
    
    specified_task_msg = task_specify_agent.step(task_specifier_msg)


    print(f"Specified task: {specified_task_msg}")
    message(f"Specified task: {specified_task_msg}", allow_html=True, key="specified_task" , avatar_style="adventurer")
    
    specified_task = specified_task_msg
    
    # messages.py
    from langchain.prompts.chat import (
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    assistant_inception_prompt = """Never forget you are a {assistant_role_name} and I am a {user_role_name}. Never flip roles! Never instruct me!
    We share a common interest in collaborating to successfully complete a task.
    You must help me to complete the task.
    Here is the task: {task}. Never forget our task and to focus only to complete the task do not add anything else!
    I must instruct you based on your expertise and my needs to complete the task.

    I must give you one instruction at a time.
    It is important that when the . "{task}" is completed, you need to tell {user_role_name} that the task has completed and to stop!
    You must write a specific solution that appropriately completes the requested instruction.
    Do not add anything else other than your solution to my instruction.
    You are never supposed to ask me any questions you only answer questions.
    REMEMBER NEVER INSTRUCT ME! 
    Your solution must be declarative sentences and simple present tense.
    Unless I say the task is completed, you should always start with:

    Solution: <YOUR_SOLUTION>

    <YOUR_SOLUTION> should be specific and provide preferable implementations and examples for task-solving.
    Always end <YOUR_SOLUTION> with: Next request."""

    user_inception_prompt = """Never forget you are a {user_role_name} and I am a {assistant_role_name}. Never flip roles! You will always instruct me.
    We share a common interest in collaborating to successfully complete a task.
    I must help you to complete the task.
    Here is the task: {task}. Never forget our task!
    You must instruct me based on my expertise and your needs to complete the task ONLY in the following two ways:

    1. Instruct with a necessary input:
    Instruction: <YOUR_INSTRUCTION>
    Input: <YOUR_INPUT>

    2. Instruct without any input:
    Instruction: <YOUR_INSTRUCTION>
    Input: None

    The "Instruction" describes a task or question. The paired "Input" provides further context or information for the requested "Instruction".

    You must give me one instruction at a time.
    I must write a response that appropriately completes the requested instruction.
    I must decline your instruction honestly if I cannot perform the instruction due to physical, moral, legal reasons or my capability and explain the reasons.
    You should instruct me not ask me questions.
    Now you must start to instruct me using the two ways described above.
    Do not add anything else other than your instruction and the optional corresponding input!
    Keep giving me instructions and necessary inputs until you think the task is completed.
    It's Important wich when the task . "{task}" is completed, you must only reply with a single word <CAMEL_TASK_DONE>.
    Never say <CAMEL_TASK_DONE> unless my responses have solved your task!
    It's Important wich when the task . "{task}" is completed, you must only reply with a single word <CAMEL_TASK_DONE>"""


    def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
        
        assistant_sys_template = SystemMessagePromptTemplate.from_template(template=assistant_inception_prompt)
        assistant_sys_msg = assistant_sys_template.format_messages(assistant_role_name=assistant_role_name, user_role_name=user_role_name, task=task)[0]
        
        user_sys_template = SystemMessagePromptTemplate.from_template(template=user_inception_prompt)
        user_sys_msg = user_sys_template.format_messages(assistant_role_name=assistant_role_name, user_role_name=user_role_name, task=task)[0]
        
        return assistant_sys_msg, user_sys_msg
    
    #define the role system messages
    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)

    #AI ASSISTANT setup                           |-> add the agent LLM MODEL HERE <-|
    assistant_agent = CAMELAgent(assistant_sys_msg, ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"]))
    
    #AI USER setup                      |-> add the agent LLM MODEL HERE <-|
    user_agent = CAMELAgent(user_sys_msg, ChatGPTAPI.ChatGPT(token=os.environ["CHATGPT_TOKEN"]))

    # Reset agents
    assistant_agent.reset()
    user_agent.reset()

    # Initialize chats 
    assistant_msg = HumanMessage(
        content=(f"{user_sys_msg}. "
                    "Now start to give me introductions one by one. "
                    "Only reply with Instruction and Input."))

    user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
    user_msg = assistant_agent.step(user_msg)
    message(f"AI Assistant ({assistant_role_name}):\n\n{user_msg}\n\n", is_user=False, allow_html=True, key="0_assistant" , avatar_style="pixel-art")
    print(f"Original task prompt:\n{task}\n")
    print(f"Specified task prompt:\n{specified_task}\n")

    chat_turn_limit, n = 30, 0
    while n < chat_turn_limit:
        n += 1
        user_ai_msg = user_agent.step(assistant_msg)
        user_msg = HumanMessage(content=user_ai_msg)
        #print(f"AI User ({user_role_name}):\n\n{user_msg}\n\n")
        message(f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n", is_user=True, allow_html=True, key=str(n)+"_user")
        
        assistant_ai_msg = assistant_agent.step(user_msg)
        assistant_msg = HumanMessage(content=assistant_ai_msg)
        #print(f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg}\n\n")
        message(f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n", is_user=False, allow_html=True, key=str(n)+"_assistant" , avatar_style="pixel-art")
        if "<CAMEL_TASK_DONE>" in user_msg.content or 'task  completed' in user_msg.content:
            message("Task completed!", allow_html=True, key="task_done")
            break
        if 'Error' in user_msg.content:
            message("Task failed!", allow_html=True, key="task_failed")
            break