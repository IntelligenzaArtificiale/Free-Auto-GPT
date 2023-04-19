from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import phind

class phindGPT4Internet(LLM):
    messages: List[Mapping[str, Any]]
    base_prompt: str 
    
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        result = phind.Completion.create(model  = 'gpt-4',
                                        prompt = prompt,
                                        results     = phind.Search.create(prompt, actualSearch = False), # create search (set actualSearch to False to disable internet)
                                        creative    = False,
                                        detailed    = False,
                                        codeContext = self.base_prompt)
        

        response = result.completion.choices[0].text
        
        self.messages.append({'role': 'user', 'content': prompt})
        self.messages.append({'role': 'assistant', 'content': response})
        
        return response
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"messages": self.messages}


#llm = phindGPT4Internet(messages=[])


#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))
