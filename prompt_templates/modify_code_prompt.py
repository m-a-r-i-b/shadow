from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def get_formatted_prompt(**kwargs):

	system_template = "You're a software engineer that when given a task and some initial code, produces updated code according to the task."
	system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)


	human_template = """
	Task: Change the add function to accept 3 arguments instead of 2.
	Initial Code:
	const add = (a,b) => (a+b);
	"""
	human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)


	ai_template = "const add = (a,b,c) => (a+b+c);"
	ai_message_prompt = AIMessagePromptTemplate.from_template(ai_template)


	user_template = """
	Task: {tasklet}
	Initial Code: 
	{initial_code}
	"""
	user_message_prompt = AIMessagePromptTemplate.from_template(user_template)

	chat_prompt = ChatPromptTemplate.from_messages(
		[system_message_prompt, human_message_prompt,ai_message_prompt,user_message_prompt]
	)

	return chat_prompt.format_prompt(**kwargs).to_messages()














# prompt_template = """"You're a software engineer that when given a task and some initial code, produces updated code according to the task.
# You should fulfill your role in the example below:

# Task: Change the add function to accept 3 arguments instead of 2.
# Initial Code:
# const add = (a,b) => (a+b);
# New Code:
# const add = (a,b,c) => (a+b+c);


# You should ALWAYS output the full code. 

# Now please help with the subtask below.

# Task: {tasklet}
# Initial Code: 
# {initial_code}
# New Code:
# """