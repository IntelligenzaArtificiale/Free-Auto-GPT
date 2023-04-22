import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import sqlchat


class sqlchatGPT3(LLM):
    
    history_data: Optional[List] = []

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        full_message = ""
        for response in sqlchat.StreamCompletion.create(prompt   = prompt,  messages = self.history_data    ):
            full_message += response.completion.choices[0].text
            
        self.history_data.append({"question": prompt, "answer": full_message})
        
        return full_message

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "sqlchat.ai"}


#llm = sqlchatGPT3()

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))