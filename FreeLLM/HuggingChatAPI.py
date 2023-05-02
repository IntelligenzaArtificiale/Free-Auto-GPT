
from hugchat import hugchat
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class HuggingChat(LLM):
    
    history_data: Optional[List] = []
    chatbot : Optional[hugchat.ChatBot] = None
    conversation : Optional[str] = ""
    
    #### WARNING : for each api call this library will create a new chat on chat.openai.com
    
    
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            pass
            #raise ValueError("stop kwargs are not permitted.")
        #token is a must check
        if self.chatbot is None:
            if self.conversation == "":
                self.chatbot = hugchat.ChatBot()
            else:
                raise ValueError("Something went wrong")
            
        
        sleep(2)
        data = self.chatbot.chat(prompt, temperature=0.5, stream=False)
        #conversation_list = self.chatbot.get_conversation_list()
        #print(conversation_list)
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":data})    
        
        return data

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "HuggingCHAT"}



#llm = HuggingChat() #for start new chat


#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well

