from dotenv import load_dotenv
load_dotenv(".env")

from shadow_agent import ShadowAgent


# prompt = "add a button to decrement count, below the increment button. After that stage, commit and then push the code in current branch"

prompt = "Hey can you increment the count by 2 when the button is pressed"

shadow_agent = ShadowAgent()
shadow_agent.run(prompt)

