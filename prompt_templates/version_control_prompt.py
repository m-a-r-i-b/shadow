from config import PROJ_ROOT_DIR
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm_bash.prompt import BashOutputParser


def get_prompt_template():
    template = """If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:
    Task: "Stage all files"
    I need to take the following actions:
    - Stage all files
    ```bash
    git add .
    ```


    Task: "Stage all files and commit the changes with message 'tooltip added'"
    I need to take the following actions:
    - Stage all files
    - Commit the changes with message 'tooltip added'
    ```bash
    git add .
    git commit -m "tooltip added"
    ```


    Task: "Stage all files, commit and push the changes to current branch"
    I need to take the following actions:
    - Stage all files
    - Commit the changes with appropriate message '<message_here>'
    - Push the changes
    ```bash
    git add .
    git commit -m "<message_here>"
    git push
    ```


    Task: "Stage, commit and push all files to a new branch called 'test-branch'"
    I need to take the following actions:
    - Create a new branch
    - Stage all files
    - Commit the changes with an appropriate message '<message_here>'
    - Push the changes to new branch
    ```bash
    git checkout -b test-branch
    git add .
    git commit -m "<message_here>"
    git push --set-upstream origin test-branch
    ```

    Remember that you need to commit changes before you push. And you need to stage changes before you commit.

    You will be optionally given some context, use this context to come up with an appropriate commit message or branch name when needed.

    You will also be given a directory path, you need to first go to that directory and then execute commands.

    That is the format. Begin!
    Directory: {root_dir}
    Context: {context}
    Task: {task}"""

    prompt_template =  PromptTemplate(
        input_variables=["task","context","root_dir"],
        template=template,
        output_parser=BashOutputParser(),
    )

    partial_prompt = prompt_template.partial(root_dir=PROJ_ROOT_DIR)

    return partial_prompt
