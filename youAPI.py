from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import you
import pydantic


class youGPT3Internet(LLM):
    
    history_data: Optional[List] = []

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = you.Completion.create(
            prompt = prompt,
            detailed     = True,
            includelinks = True,
            chat=self.history_data
        )

        text = response["response"]

        self.history_data.append({"question": prompt, "answer": response["response"]})
        
        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "davinci"}


#llm = youGPT3Internet()

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))
