from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
from prompt_templates.shadow_prompt import get_prompt_template
from tools.modify_code_tool import ModifyCodeTool
from tools.version_control_tool import VersionControlTool
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory


from config import MODIFY_CODE_TOOL_LLM, MODIFY_CODE_TOOL_TEMP, SHADOW_AGENT_TEMP, SHADOW_AGENT_LLM, VERSION_CONTROL_TOOL_LLM, VERSION_CONTROL_TOOL_TEMP


class ShadowAgent:
    def __init__(self) -> None:

        # llm = OpenAI(model=SHADOW_AGENT_LLM)
        llm = ChatOpenAI(temperature=SHADOW_AGENT_TEMP, model=SHADOW_AGENT_LLM)
        output_parser = CustomOutputParser()

        tools = self.get_tools()

        # LLM chain consisting of the LLM and a prompt
        llm_chain = LLMChain(llm=llm, prompt=get_prompt_template(tools), verbose=True)
        tool_names = [tool.name for tool in tools]
        memory = ConversationBufferWindowMemory(k=2)


        agent_template = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            # TODO : Figure out if this STOP and AGENTFINISH are correlated
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        self._agent = AgentExecutor.from_agent_and_tools(
            agent=agent_template, tools=tools, verbose=True,memory=memory)


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
            name="ModifyCodeTool",
            func=ModifyCodeTool(ChatOpenAI())._execute_task,
            description="""Use it to change an existing code file""",
        ),
        ]




class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        # TODO : Figure out of the STOP above is correlated
        if "Final Answer:" in llm_output or "Job is done" in llm_output or "I have now performed all tasks" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


