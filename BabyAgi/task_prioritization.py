from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel


class TaskPrioritizationChain(LLMChain):
    """Chain to prioritize tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        task_prioritization_template = (
            "Please help me to cleaning the formatting of "
            "and reprioritizing the following tasks: {task_names}."
            "Consider the ultimate objective of your team: {objective}."
            "Do not remove any tasks. Return ONLY the result as a numbered list without anything else, like:\n"
            "1. First task\n"
            "2. Second task\n"
            "Start the task list with number {next_task_id}."
        )
        prompt = PromptTemplate(
            template=task_prioritization_template,
            input_variables=["task_names", "next_task_id", "objective"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
