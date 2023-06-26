from prompt_templates.version_control_prompt import get_prompt_template
from prompt_templates.modify_code_prompt import get_formatted_prompt
import time
from langchain.chains import LLMBashChain

class VersionControlTool():
    def __init__(self, llm) -> None:
        self.bash_chain = LLMBashChain.from_llm(llm, prompt=get_prompt_template(), verbose=True)

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