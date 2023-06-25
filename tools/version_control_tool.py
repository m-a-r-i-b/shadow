from tools.base_tool import BaseTool
from prompt_templates.modify_code_prompt import prompt_template

class VersionControlTool(BaseTool):
    def __init__(self, llm) -> None:
        self.llm = llm
        self._prompt = prompt_template


    def execute_task(self, tasklet):
        return "Job is done"
    

    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]
        return result