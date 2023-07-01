from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm_bash.prompt import BashOutputParser


def get_prompt_template():
    prompt_template = """If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:
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
    - Commit the changes with appropriate message '<message_here>'
    - Push the changes
    ```bash
    git checkout -b test-branch
    git add .
    git commit -m "<message_here>"
    git push
    ```

    Remember that you need to commit changes before you push. And you need to stage changes before you commit.

    That is the format. Begin!
    Task: {question}"""

    # TODO : For some reason only 'question' variable is accepted, nothing else works
    return PromptTemplate(
        input_variables=["question"],
        template=prompt_template,
        output_parser=BashOutputParser(),
    )
