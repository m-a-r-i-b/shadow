from prompt_templates.version_control_template import get_prompt_template
from langchain.chains import LLMBashChain

class VersionControlTool():
    def __init__(self, llm) -> None:
        self._prompt_template = get_prompt_template()
        self._bash_chain = LLMBashChain.from_llm(llm, verbose=True)


    def execute_task(self, task, context):
        prompt = self._prompt_template.format(task=task,context=context)
        self._bash_chain.run(prompt)
    