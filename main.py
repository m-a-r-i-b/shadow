from dotenv import load_dotenv
load_dotenv(".env")

from shadow_agent import ShadowAgent


# instructions = "add a button to decrement count below the increment button. After that stage, commit and push the code in current branch with appropriate commit message"
# instructions = "add a button to decrement count, below the increment button. After that stage, commit and then push the code in current branch"
# instructions = "hey can you add a button to decrement count, below the increment button and then push the code"
# instructions = "hey can you add a button to decrement count, below the increment button and then push the changes"
instructions = "hey can you add a button to decrement count, below the increment button and then push the changes to a new branch"
# instructions = "Change the increment logic to add 2"

shadow_agent = ShadowAgent()
shadow_agent.execute(instructions)

