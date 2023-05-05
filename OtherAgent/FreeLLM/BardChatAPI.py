from Bard import Chatbot
import asyncio

import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class BardChat(LLM):
    
    history_data: Optional[List] = []
    cookie : Optional[str]
    chatbot : Optional[Chatbot] = None

    
    @property
    def _llm_type(self) -> str:
        return "custom"

    async def call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            pass
            #raise ValueError("stop kwargs are not permitted.")
        #cookie is a must check
        if self.chatbot is None:
            if self.cookie is None:
                raise ValueError("Need a COOKIE , check https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required for get your COOKIE AND SAVE")
            else:
                #if self.chatbot == None:
                self.chatbot = Chatbot(self.cookie)
               
        response = self.chatbot.ask(prompt)
        #print(response)
        response_text = response['content']
        #add to history
        self.history_data.append({"prompt":prompt,"response":response_text})    
        
        return response_text
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return asyncio.run(self.call(prompt=prompt))

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "BardCHAT", "cookie": self.cookie}



#llm = BardChat(cookie = "YOURCOOKIE") #for start new chat

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well
