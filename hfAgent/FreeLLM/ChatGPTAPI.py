from gpt4_openai import GPT4OpenAI
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from time import sleep



class ChatGPT(LLM):
    
    history_data: Optional[List] = []
    token : Optional[str]
    chatbot : Optional[GPT4OpenAI] = None
    call : int = 0
    model : str = "gpt-3" # or gpt-4
    plugin_id : Optional[List] = []
    
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
            if self.token is None:
                raise ValueError("Need a token , check https://chat.openai.com/api/auth/session for get your token")
            else:
                try:
                    if self.plugin_id == []:
                        self.chatbot = GPT4OpenAI(token=self.token, model=self.model)
                    else:
                        self.chatbot = GPT4OpenAI(token=self.token, model=self.model, plugin_ids=self.plugin_id)
                except:
                    raise ValueError("Error on create chatbot, check your token, or your model")
                
        response = ""
        # OpenAI: 50 requests / hour for each account
        if (self.call >= 45 and self.model == "default") or (self.call >= 23 and self.model == "gpt4"):
            raise ValueError("You have reached the maximum number of requests per hour ! Help me to Improve. Abusing this tool is at your own risk")
        else:
            sleep(2)
            response = self.chatbot(prompt)
            
            self.call += 1
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":response})    
        
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "ChatGPT", "token": self.token, "model": self.model}



#llm = ChatGPT(token = "YOUR-COOKIE") #for start new chat

#llm = ChatGPT(token = "YOUR-COOKIE" , model="gpt4") # REQUIRED CHATGPT PLUS subscription

#llm = ChatGPT(token = "YOUR-COOKIE", conversation = "Add-XXXX-XXXX-Convesation-ID") #for use a chat already started

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well
