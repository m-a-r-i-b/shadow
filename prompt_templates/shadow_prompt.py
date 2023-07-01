from typing import List, Union
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool


# TODO : Modify prompt to better formulate 'action input'

# Set up the base template
prompt_template = """You will be given instruction to perform tasks. You have access to the following tools:

{tools}

Use the following format:

Task: the task you must perform
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: Short summary of previous task + a part of the original instruction, should be from "{input}".
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have now performed all tasks
Final Answer: the final answer to the original task

Begin!

Previous conversation history:
{history}

New Task: {input}
{agent_scratchpad}"""


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)



def get_prompt_template(tools):
    return CustomPromptTemplate(
        template=prompt_template,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps","history"]
    )
