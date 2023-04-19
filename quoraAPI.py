from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import quora
import pydantic


class GPT4QUORA(LLM):
    
    conversation_id: Optional[str]
    token: Optional[quora.Account] = None
    
    def __init__(self, conversation_id: Optional[str] = None):
        super().__init__()
        self.conversation_id = conversation_id

        if self.conversation_id is None:
            # If no conversation ID is provided, start a new conversation
            if self.token is None:
                self.token = quora.Account.create(logging = True, enable_bot_creation=True)



    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # GPT4 have one limit request for account , try to buypass this limit
        response = quora.Completion.create(model  = 'gpt-3.5-turbo',
                                            prompt = prompt,
                                            token  = self.token)


        text = response.completion.choices[0].text

        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"conversation_id": self.conversation_id}


#llm = GPT4ORA()

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))