from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage



prompt_template = """"You're a software engineer that when given a task and initial code, produces new code.
You should fulfill your role in the example below:

Task: Change the add function to accept 3 arguments instead of 2.
Initial Code:
const add = (a,b) => (a+b);
New Code:
const add = (a,b,c) => (a+b+c);


You should ALWAYS output the full code. 

Now please help with the subtask below.

Task: {tasklet}
Initial Code: 
{initial_code}
New Code:
"""


template = (
    "You are a helpful assistant that translates {input_language} to {output_language}."
)
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)