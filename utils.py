from typing import List
from langchain.agents import Tool
from tools.modify_code_tool import ModifyCodeTool
from tools.version_control_tool import VersionControlTool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


def get_tool_list() -> List[Tool]: 
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