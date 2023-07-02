from prompt_templates.version_control_prompt import get_prompt_template
from prompt_templates.modify_code_prompt import get_formatted_prompt
import time
from langchain.chains import LLMBashChain

class VersionControlTool():
    def __init__(self, llm) -> None:
        self._prompt_template = get_prompt_template()
        self.bash_chain = LLMBashChain.from_llm(llm, verbose=True)


    def _execute_task(self, task, context):
        prompt = self._prompt_template.format(question=task,context=context)
        self.bash_chain.run(prompt)
    

    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]
        return result