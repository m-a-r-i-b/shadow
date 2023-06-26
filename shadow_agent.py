from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from dotenv import load_dotenv
load_dotenv(".env")

from config import MODIFY_CODE_TOOL_LLM, MODIFY_CODE_TOOL_TEMP, SHADOW_AGENT_TEMP, SHADOW_AGENT_LLM, VERSION_CONTROL_TOOL_LLM, VERSION_CONTROL_TOOL_TEMP
from tools.modify_code_tool import ModifyCodeTool
from tools.version_control_tool import VersionControlTool


class ShadowAgent:
    def __init__(self) -> None:

        # llm = OpenAI(model=SHADOW_AGENT_LLM)
        llm = ChatOpenAI(temperature=SHADOW_AGENT_TEMP, model=SHADOW_AGENT_LLM)
        self._agent = initialize_agent(
            self.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

    def run(self,task):
        self._agent.run(task)

    def get_tools(self):
        return [
        Tool(
            name="VersionControlTool",
            func=VersionControlTool(OpenAI())._execute_task,
            description="""Use it to commit changes to a git repo or create new git branches""",
        ),
        Tool(
            name="ChangeCodeTool",
            func=ModifyCodeTool(ChatOpenAI())._execute_task,
            description="""Use it to change an existing code file""",
        ),
        ]