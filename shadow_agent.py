from typing import List
from models.Task import Task
from models.TaskList import TaskList
from prompt_templates.shadow_prompt import get_prompt_template
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import Tool


from config import SHADOW_AGENT_TEMP, SHADOW_AGENT_LLM
from utils import get_tool_list


# TODO:
# 4 - Add whisper ai


class ShadowAgent:
    def __init__(self) -> None:
        self._llm = OpenAI(temperature=SHADOW_AGENT_TEMP, model=SHADOW_AGENT_LLM)
        self._tools : List[Tool] = get_tool_list()
        self._parser = PydanticOutputParser(pydantic_object=TaskList)
        self._prompt_template = get_prompt_template(self._tools,self._parser)
        self._context = ""

    def get_tool(self, tool_name: str):
        for tool in self._tools:
            if tool.name.strip() == tool_name.strip():
                return tool.func


    def perform_task(self, task: Task):
        tool_name = task.tool_name
        tool = self.get_tool(tool_name)
        instruction = task.instruction
        tool(instruction, self._context)


    def execute(self,instructions):
        _input = self._prompt_template.format(instruction=instructions)
        output = self._llm(_input)
        task_list: TaskList = self._parser.parse(output)

        print(task_list)
        print("="*20)

        for task in task_list:
            print("-"*20)
            print("Tool Name = ",task.tool_name)
            print("Instruction = ",task.instruction)
            self.perform_task(task)
            self._context += task.instruction+"\n"


