from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import writesonic
import pydantic


class writesonicGPT3Internet(LLM):
    
    history_data: Optional[List[Mapping[str, Any]]] = []
    token: Optional[writesonic.Account] = writesonic.Account.create(logging = True)



    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # GPT4 have one limit request for account , try to buypass this limit
        response =  writesonic.Completion.create(api_key= self.token.key,
                                            prompt = prompt,
                                            enable_memory = True,
                                            history_data= self.history_data,
                                            enable_google_results = True)


        text = response.completion.choices[0].text

        self.history_data.append({'is_sent': True, 'message': prompt})
        self.history_data.append({'is_sent': False, 'message': text})
        
        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"conversation_id": self.token}


#llm = writesonicGPT3Internet()

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))