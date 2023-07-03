from typing import List
from langchain.agents import Tool
from tools.modify_code_tool import ModifyCodeTool
from tools.version_control_tool import VersionControlTool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from config import ACCEPTABLE_FILE_TYPES


def acceptable_file_type(file):
    for fileType in ACCEPTABLE_FILE_TYPES:
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