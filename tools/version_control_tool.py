from tools.base_tool import BaseTool
from prompt_templates.modify_code_prompt import get_formatted_prompt
import time
from langchain.chains import LLMBashChain

class VersionControlTool(BaseTool):
    def __init__(self, llm) -> None:
        self.bash_chain = LLMBashChain.from_llm(llm, verbose=True)

        # self._prompt = get_formatted_prompt


    def _execute_task(self, tasklet):
        print("received arg = ",tasklet)

        print("===Before===")
        self.bash_chain.run(tasklet)
        print("====After===")


        time.sleep(2)
        return "Job is done"
    

    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]
        return result