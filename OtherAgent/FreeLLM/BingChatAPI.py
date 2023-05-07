from EdgeGPT import Chatbot, ConversationStyle
import asyncio

import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class BingChat(LLM):
    
    history_data: Optional[List] = []
    cookiepath : Optional[str]
    chatbot : Optional[Chatbot] = None
    conversation_style : Optional[str] 
    conversation_style_on : Optional[ConversationStyle] = ConversationStyle.precise
    search_result : Optional[bool] = False
    
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def select_conversation(self, conversation_style: str):
        if conversation_style == "precise":
            self.conversation_style_on = ConversationStyle.precise
        elif conversation_style == "creative":
            self.conversation_style_on = ConversationStyle.creative
        elif conversation_style == "balanced":
            self.conversation_style_on = ConversationStyle.balanced
        else:
            raise ValueError("conversation_style must be precise, creative or balaced")
        self.conversation_style = conversation_style

    async def call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            pass
            #raise ValueError("stop kwargs are not permitted.")
        #cookiepath is a must check
        if self.chatbot is None:
            if self.cookiepath is None:
                raise ValueError("Need a COOKIE , check https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required for get your COOKIE AND SAVE")
            else:
                #if self.chatbot == None:
                self.chatbot = await Chatbot.create(cookie_path=self.cookiepath)
               
        if self.conversation_style is not None:
            self.conversation_style_on = self.select_conversation(self.conversation_style)
            
        response = await self.chatbot.ask(prompt=prompt, conversation_style=self.conversation_style, search_result=self.search_result)
        response_messages = response.get("item", {}).get("messages", [])
        response_text = response_messages[1].get("text", "")
        
        if response_text == "":
            hidden_text = response_messages[1].get("hiddenText", "")
            print(">>>> [DEBBUGGER] hidden_text = " + str(hidden_text) + " [DEBBUGGER] <<<<")
            print(">>>> [DEBBUGGER] BING CHAT dont is open Like CHATGPT , BingCHAT have refused to respond. [DEBBUGGER] <<<<")
            response_text = hidden_text
            """
            # reset the chatbot and remake the call
            print("[DEBUGGER] Chatbot failed to respond. Resetting and trying again. [DEBUGGER]")
            print("[ INFO DEBUGGER ] \n<Response>\n" + str(response) + "\n</Response>\n\n")
            sleep(10)
            self.chatbot = await Chatbot.create(cookie_path=self.cookiepath)
            sleep(2)
            response = await self.chatbot.ask(prompt=prompt)
            response_messages = response.get("item", {}).get("messages", [])
            response_text = response_messages[1].get("text", "")
            """
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":response_text})    
        
        return response_text
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return asyncio.run(self.call(prompt=prompt))

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "BingCHAT", "cookiepath": self.cookiepath}



#llm = BingChat(cookiepath = "YOUR-COOKIE") #for start new chat
#llm = BingChat(cookiepath = "YOUR-COOKIE", conversation_style = "precise") #precise, creative or balaced
#llm = BingChat(cookiepath = "YOUR-COOKIE" , conversation_style = "precise" , search_result=True) #with web access

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well
