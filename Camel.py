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
from t3nsorAPI import gpt3NoInternet
from message import get_sys_msgs 
import streamlit as st
from streamlit_chat_media import message

    
class CAMELAgent:

    def __init__(
        self,
        system_message: SystemMessage,
        model: gpt3NoInternet(messages=[]),
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

if st.button("Start Autonomus AI AGENT"):
    task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
    task_specifier_prompt = (
    """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
    Please make it more specific. Be creative and imaginative.
    Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
    )
    task_specifier_template = HumanMessagePromptTemplate.from_template(template=task_specifier_prompt)
    
    task_specify_agent = CAMELAgent(task_specifier_sys_msg, gpt3NoInternet(messages=[]))
    task_specifier_msg = task_specifier_template.format_messages(assistant_role_name=assistant_role_name,
                                                                user_role_name=user_role_name,
                                                                task=task, word_limit=word_limit)[0]
    
    specified_task_msg = task_specify_agent.step(task_specifier_msg)


    print(f"Specified task: {specified_task_msg}")
    message(f"Specified task: {specified_task_msg}", allow_html=True, key="specified_task" , avatar_style="adventurer")
    
    specified_task = specified_task_msg


    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)
    assistant_agent = CAMELAgent(assistant_sys_msg, gpt3NoInternet(messages=[]))
    user_agent = CAMELAgent(user_sys_msg, gpt3NoInternet(messages=[]))

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

    chat_turn_limit, n = 300, 0
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
        if "<CAMEL_TASK_DONE>" in user_msg.content:
            message("Task completed!", allow_html=True, key="task_done")
            break
        if 'Error' in user_msg.content:
            message("Task failed!", allow_html=True, key="task_failed")
            break