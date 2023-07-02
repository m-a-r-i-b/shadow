from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from prompt_templates.shadow_prompt import get_prompt_template
from pydantic import BaseModel, Field
from typing import List

from langchain.agents import Tool
from dotenv import load_dotenv
from tools.modify_code_tool import ModifyCodeTool
from tools.version_control_tool import VersionControlTool


load_dotenv(".env")


def get_tools():
    return [
        Tool(
            name="VersionControlTool",
            func=VersionControlTool(OpenAI())._execute_task,
            description="""Use it to stage, commit or push changes to a git repo or create new branches""",
        ),
        Tool(
            name="ModifyCodeTool",
            func=ModifyCodeTool(ChatOpenAI())._execute_task,
            description="""Use it to change an existing code file""",
        ),
    ]


class Task(BaseModel):
    tool: str = Field(description="The tool to be used")
    instruction: str = Field(description="The instruction for the tool")


class TaskList(BaseModel):
  
    taskList: List[Task]

    def __iter__(self):
        return iter(self.taskList)

    def __getitem__(self, item):
        return self.taskList[item]


model_name = "text-davinci-003"
temperature = 0.0
model = OpenAI(model_name=model_name, temperature=temperature)



instruc = "add a button to decrement count, below the increment button. After that stage, commit and then push the code in current branch"
# instruc = "Change the increment logic to add 2 every time a button is pressed"


parser = PydanticOutputParser(pydantic_object=TaskList)

prompt_template = get_prompt_template(get_tools())

# print(prompt_template)
# print("-"*20)
# print(prompt_template.format(format_instructions="Some formating instructions",instruction="INSTRC"))


_input = prompt_template.format(format_instructions=parser.get_format_instructions(),instruction=instruc)

print(_input)

output = model(_input)

res = parser.parse(output)


print(res)

for task in res:
    print("T = ",task.tool)
    print("T = ",task.instruction)