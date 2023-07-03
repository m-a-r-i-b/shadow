from typing import List
from langchain.agents import Tool
from tools.ModifyCodeTool import ModifyCodeTool
from tools.VersionControlTool import VersionControlTool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


def is_acceptable_file_type(file, acceptable_file_types):
    for fileType in acceptable_file_types:
        if file.endswith(fileType):
            return True
    return False


def get_tool_list() -> List[Tool]: 
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