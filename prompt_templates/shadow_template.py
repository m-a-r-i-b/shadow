from typing import List
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool
from langchain.output_parsers import PydanticOutputParser


class CustomPromptTemplate(StringPromptTemplate):

    # The template to use
    template: str

    # The list of tools available
    tools: List[Tool]

    # Output parser
    parser: PydanticOutputParser


    def format(self, **kwargs) -> str:
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])

        kwargs["format_instructions"] = self.parser.get_format_instructions()
        return self.template.format(**kwargs)



def get_prompt_template(tools, parser):

    # Set up the base template
    prompt_template = """You will be given instruction to perform tasks. You have access to the following tools:

{tools}

Your job is to break down the task into sub tasks for each of the available tools. When creating sub tasks, do not rephrase or add own assumptions.

Also, assign the tool to be used for each sub task, the tool name should be one of [{tool_names}]

{format_instructions}

Begin!

New Task: {instruction}
    """

    return CustomPromptTemplate(
        template=prompt_template,
        tools=tools,
        input_variables=["instruction"],
        parser=parser
    )
