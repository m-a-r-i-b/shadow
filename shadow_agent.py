import os
from typing import List
from models.Task import Task
from models.TaskList import TaskList
from prompt_templates.shadow_template import get_prompt_template
import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import Tool

from tools.ModifyCodeTool import ModifyCodeTool
from tools.VersionControlTool import VersionControlTool

from config import SHADOW_AGENT_TEMP, SHADOW_AGENT_LLM


class ShadowAgent:
    def __init__(self) -> None:
        self._llm = OpenAI(temperature=SHADOW_AGENT_TEMP, model=SHADOW_AGENT_LLM)
        self._tools : List[Tool] = self._get_tool_list()
        self._parser = PydanticOutputParser(pydantic_object=TaskList)
        self._prompt_template = get_prompt_template(self._tools,self._parser)
        self._context = ""

    def _get_tool_list(self) -> List[Tool]:
        return [
            Tool(
                name="VersionControlTool",
                func=VersionControlTool(OpenAI()).execute_task,
                description="""Use it to stage, commit or push changes to a git repo or create new branches""",
            ),
            Tool(
                name="ModifyCodeTool",
                func=ModifyCodeTool(ChatOpenAI()).execute_task,
                description="""Use it to change an existing code file""",
            ),
        ]


    def _get_tool(self, tool_name: str):
        for tool in self._tools:
            if tool.name.strip() == tool_name.strip():
                return tool.func


    def _perform_task(self, task: Task):
        tool_name = task.tool_name
        tool = self._get_tool(tool_name)
        instruction = task.instruction
        tool(instruction, self._context)


    def _split_into_tasks(self, instructions:str):
        _input = self._prompt_template.format(instruction=instructions)
        output = self._llm(_input)
        task_list: TaskList = self._parser.parse(output)
        return task_list


    def _get_text_from_audio(self,audio_file) -> str:
        # For some reason need to explicitly do this for openai.Audio, even tho dotenv is being loaded
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print("Generating transcriptions...")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text

    def execute(self,text_instructions=None, audio_instructions=None):

        if text_instructions is None and audio_instructions is None:
            print("No instructions to exectue..")

        if audio_instructions:
            instructions = self._get_text_from_audio(audio_instructions)

        if text_instructions:
            instructions = text_instructions
        
        task_list = self._split_into_tasks(instructions)

        print(task_list)
        print("="*20)

        for task in task_list:
            print("-"*20)
            print("Tool Name = ",task.tool_name)
            print("Instruction = ",task.instruction)
            # self._perform_task(task)
            self._context += task.instruction+"\n"


