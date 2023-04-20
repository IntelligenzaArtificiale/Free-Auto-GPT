from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import quora
import pydantic


class GPT4QUORA(LLM):
    
    token: Optional[quora.Account] = quora.Account.create(logging = True, enable_bot_creation=True)
    


    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # GPT4 have one limit request for account , try to buypass this limit
        response = quora.Completion.create(model  = 'gpt-4',
                                            prompt = prompt,
                                            token  = self.token)


        text = response.completion.choices[0].text

        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "GPT4"}


#llm = GPT4QUORA()

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))