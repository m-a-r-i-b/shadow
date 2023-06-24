from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from dotenv import load_dotenv
load_dotenv(".env")

from config import SHADOW_AGENT_LLM, CHANGE_CODE_AGENT_LLM,VERSION_CONTROL_AGENT_LLM
from sub_agents.change_code import ChangeCodeAgent
from sub_agents.version_control import VersionControlAgent


class ShadowAgent:
    def __init__(self) -> None:

        # llm = OpenAI(model=SHADOW_AGENT_LLM)
        llm = ChatOpenAI(temperature=0.1, model=SHADOW_AGENT_LLM)
        self._agent = initialize_agent(
            self.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

    def run(self,task):
        self._agent.run(task)

    def get_tools(self):
        return [
        Tool(
            name="VersionControlTool",
            func=VersionControlAgent(OpenAI()).execute_task,
            description="""Use it to commit changes to a git repo or create new git branches""",
        ),
        Tool(
            name="ChangeCodeTool",
            func=ChangeCodeAgent(OpenAI()).execute_task,
            description="""Use it to change an existing code file""",
        ),
        ]