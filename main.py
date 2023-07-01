from dotenv import load_dotenv
load_dotenv(".env")

from shadow_agent import ShadowAgent


# prompt = "add a button to decrement count below the increment button. Once done, commit code with appropriate message"
# prompt = "add a button to decrement count below the increment button. After that stage, commit and push the code in current branch with appropriate commit message"
prompt = "add a button to decrement count, below the increment button. After that stage, commit and then push the code in current branch with some commit message 'changes done'"

shadow_agent = ShadowAgent()
shadow_agent.run(prompt)

