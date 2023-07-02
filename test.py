from dotenv import load_dotenv

from utils import get_tool_list
load_dotenv(".env")


tools = get_tool_list()
vc = tools[0].func

prompt = 'Stage, commit and then push the code in current branch'
context = "added decrement button"

vc(prompt,context)

